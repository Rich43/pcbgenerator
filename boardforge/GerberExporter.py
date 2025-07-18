import os
import zipfile
import shutil
from pathlib import Path

def export_gerbers(board, output_zip_path):
    """
    Export board layers as Gerber files and compress them into a ZIP archive.
    
    Args:
        board: Object containing layer data with 'layers' attribute (dict) and save_svg_previews method
        output_zip_path: Path where the ZIP file will be saved
    """
    try:
        # Convert to Path object for better path handling
        output_zip_path = Path(output_zip_path)
        # Ensure parent directory exists
        output_zip_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create temporary directory for Gerber files
        temp_dir = output_zip_path.parent / "temp_gerbers"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Gerber files for each layer
        for layer_name, content in board.layers.items():
            filename = temp_dir / f"{layer_name}.gbr"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"G04 {layer_name} *\n")
                # Ensure content is iterable and handle potential None values
                if content:
                    for line in content:
                        if isinstance(line, tuple) and line[0] == "TRACE":
                            pin1, pin2 = line[1], line[2]
                            # Optional width stored at line[3]
                            x1 = int(pin1.x * 1000)
                            y1 = int(pin1.y * 1000)
                            x2 = int(pin2.x * 1000)
                            y2 = int(pin2.y * 1000)
                            f.write(f"X{x1:07d}Y{y1:07d}D02*\n")
                            f.write(f"X{x2:07d}Y{y2:07d}D01*\n")
                        elif isinstance(line, tuple) and line[0] == "TRACE_PATH":
                            pts = line[1]
                            # line[2] may contain width
                            for i in range(len(pts) - 1):
                                x1 = int(pts[i][0] * 1000)
                                y1 = int(pts[i][1] * 1000)
                                x2 = int(pts[i + 1][0] * 1000)
                                y2 = int(pts[i + 1][1] * 1000)
                                f.write(f"X{x1:07d}Y{y1:07d}D02*\n")
                                f.write(f"X{x2:07d}Y{y2:07d}D01*\n")
                        else:
                            f.write(f"{line}\n")

        # Drill/hole file
        if getattr(board, "holes", None):
            import math
            holes_path = temp_dir / "holes.gbr"
            with open(holes_path, "w", encoding="utf-8") as f:
                f.write("G04 holes *\n")
                for hx, hy, dia, ann in board.holes:
                    r = dia / 2.0
                    for i in range(13):
                        a = 2 * math.pi * i / 12
                        x = hx + r * math.cos(a)
                        y = hy + r * math.sin(a)
                        code = "D02*" if i == 0 else "D01*"
                        f.write(f"X{int(x*1000):07d}Y{int(y*1000):07d}{code}\n")
                    if ann is not None:
                        rr = r + ann
                        for i in range(13):
                            a = 2 * math.pi * i / 12
                            x = hx + rr * math.cos(a)
                            y = hy + rr * math.sin(a)
                            code = "D02*" if i == 0 else "D01*"
                            f.write(f"X{int(x*1000):07d}Y{int(y*1000):07d}{code}\n")
        
        # Save SVG previews if the method exists
        if hasattr(board, 'save_svg_previews'):
            board.save_svg_previews(str(temp_dir))
        
        # Prepare exploded output directory and ZIP archive
        exploded_dir = output_zip_path.parent / output_zip_path.stem
        exploded_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_dir.glob("*"):
                if file_path.is_file():
                    zipf.write(file_path, file_path.name)
                    shutil.copy(file_path, exploded_dir / file_path.name)
    
    except Exception as e:
        print(f"Error during Gerber export: {str(e)}")
        raise
    
    finally:
        # Clean up temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
