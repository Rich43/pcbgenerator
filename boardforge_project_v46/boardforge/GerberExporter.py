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
                        f.write(f"{line}\n")
        
        # Save SVG previews if the method exists
        if hasattr(board, 'save_svg_previews'):
            board.save_svg_previews(str(temp_dir))
        
        # Create ZIP archive
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_dir.glob("*"):
                if file_path.is_file():
                    # Use relative path in ZIP to avoid including full directory structure
                    zipf.write(file_path, file_path.name)
    
    except Exception as e:
        print(f"Error during Gerber export: {str(e)}")
        raise
    
    finally:
        # Clean up temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
