"""
Image Optimization Utility
Supports WebP conversion, Progressive JPEG, and compression
"""
import os
from PIL import Image
import io

def optimize_image(input_path, output_path=None, quality=85, format='auto', progressive=True):
    """
    Optimize an image file
    
    Args:
        input_path: Path to input image
        output_path: Path to output image (if None, overwrites input)
        quality: JPEG/WebP quality (1-100, default 85)
        format: 'auto', 'webp', 'jpeg', 'png' (auto detects best format)
        progressive: Use progressive JPEG (default True)
    
    Returns:
        Output file path
    """
    try:
        # Open image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB for JPEG
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Determine output format
        if format == 'auto':
            # Use WebP for better compression, fallback to JPEG
            if output_path and output_path.lower().endswith('.webp'):
                format = 'WEBP'
            elif output_path and output_path.lower().endswith('.png'):
                format = 'PNG'
            else:
                format = 'JPEG'
        
        # Set output path
        if output_path is None:
            output_path = input_path
        
        # Save optimized image
        save_kwargs = {
            'optimize': True,
            'quality': quality
        }
        
        if format == 'JPEG' and progressive:
            save_kwargs['progressive'] = True
        
        img.save(output_path, format=format, **save_kwargs)
        
        return output_path
    
    except Exception as e:
        print(f"Error optimizing image {input_path}: {e}")
        return None

def create_webp_version(input_path, output_path=None, quality=85):
    """
    Create WebP version of an image
    
    Args:
        input_path: Path to input image
        output_path: Path to output WebP (if None, creates .webp version)
        quality: WebP quality (1-100, default 85)
    
    Returns:
        Output file path
    """
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Set output path
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}.webp"
        
        # Save as WebP
        img.save(output_path, format='WEBP', quality=quality, method=6)
        
        return output_path
    
    except Exception as e:
        print(f"Error creating WebP version {input_path}: {e}")
        return None

def compress_image(input_path, output_path=None, max_size_kb=500, quality=85):
    """
    Compress image to target file size
    
    Args:
        input_path: Path to input image
        output_path: Path to output image (if None, overwrites input)
        max_size_kb: Maximum file size in KB (default 500)
        quality: Starting quality (default 85)
    
    Returns:
        Output file path
    """
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB for JPEG
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Set output path
        if output_path is None:
            output_path = input_path
        
        # Try different quality levels to meet size target
        current_quality = quality
        min_quality = 50
        
        while current_quality >= min_quality:
            # Save to memory first to check size
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=current_quality, progressive=True, optimize=True)
            size_kb = len(buffer.getvalue()) / 1024
            
            if size_kb <= max_size_kb:
                # Save to file
                buffer.seek(0)
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return output_path
            
            current_quality -= 5
        
        # If still too large, save with minimum quality
        img.save(output_path, format='JPEG', quality=min_quality, progressive=True, optimize=True)
        return output_path
    
    except Exception as e:
        print(f"Error compressing image {input_path}: {e}")
        return None

def optimize_directory(directory_path, recursive=True, quality=85, create_webp=True):
    """
    Optimize all images in a directory
    
    Args:
        directory_path: Path to directory
        recursive: Process subdirectories (default True)
        quality: Image quality (default 85)
        create_webp: Create WebP versions (default True)
    """
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp')
    processed = 0
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(supported_formats):
                input_path = os.path.join(root, file)
                
                # Optimize original
                optimize_image(input_path, quality=quality, progressive=True)
                
                # Create WebP version if requested
                if create_webp and not file.lower().endswith('.webp'):
                    create_webp_version(input_path, quality=quality)
                
                processed += 1
                print(f"Optimized: {input_path}")
        
        if not recursive:
            break
    
    print(f"Processed {processed} images")
    return processed

