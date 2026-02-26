import sys
from PIL import Image, ImageChops

def trim(im):
    # Convert image to RGB for accurate trimming of whitespace
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def main():
    try:
        im = Image.open('assets/logo-r1.jpg').convert('RGB')
        # find the true bounding box, white is (255, 255, 255)
        # However, due to JPG compression, white might be not exactly 255.
        # A simpler way to get bounding box:
        # threshold the image
        gray = im.convert('L')
        # Anything below 240 is considered part of the image
        bbox = gray.point(lambda p: p > 240 and 255).getbbox()
        
        trimmed = im
        if bbox:
            print(f"Trimming image based on bounding box: {bbox}")
            # we can inverted the threshold since getbbox() gets the bounding box of non-zero regions.
            bw = gray.point(lambda x: 0 if x > 240 else 255, '1')
            actual_bbox = bw.getbbox()
            if actual_bbox:
                print(f"Actual content box: {actual_bbox}")
                trimmed = im.crop(actual_bbox)
        
        # Save as transparent PNG
        # Convert to RGBA
        rgba = trimmed.convert('RGBA')
        data = rgba.getdata()
        
        # We can make white transparent
        new_data = []
        for item in data:
            if item[0] > 230 and item[1] > 230 and item[2] > 230:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        rgba.putdata(new_data)
        
        rgba.save('assets/logo-r1-cropped.png', 'PNG')
        print("Done cropping and saving background-free PNG!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
