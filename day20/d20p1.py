import fileinput

# Load the source data in from a file
def load_input_data():
    global iea, image, image_height, image_width

    # Load in the Image Enhancement Algorithm (iea) and the image data
    for line in fileinput.input():
        line = line.rstrip()                        # Clean up any spare characters on the end

        if iea == "":
            iea = line
        elif line == "":
            continue
        else:
            image_width = len(line)
            image_height += 1
            # Grow the image left and right be extra_image_space dark pixels
            extra = "." * extra_image_space
            image.append(list(extra + line + extra))

    # Expand the image top and bottom by extra_image_space rows of dark pixels
    for i in range(0, extra_image_space):
        image.insert(0, list("." * (image_width + (2 * extra_image_space))))
    for i in range(0, extra_image_space):
        image.append(list("." * (image_width + (2 * extra_image_space))))

    image_width = len(image[0])
    image_height = len(image)

# Display the top left of the image grid
def display_image(image, rows, cols):
    for row in image[:rows]:
        print(''.join(row[:cols]))
    print()             # Print a blank line after the image for readability

# Take a string of . and # and turn it into 0 and 1
def pixels_to_binary(pixels):
    pixels = pixels.replace(".", "0")
    pixels = pixels.replace("#", "1")
    return pixels

# Take a binary number in a string and return a decimal integer
def binary_string_to_decimal(binary_string):
    return(int(binary_string, 2))

# Lookup the value of a pixel and if it is out of bounds then return a dark pixel
# The parameters are y, x because I changed how this worked and it was easier to re-order the parameters here
# than change all the placed it was called. Hackery 101: it's easier to do the hack and comment it than it is
# to re-write the code properly!
def lookup_pixel(y, x):
    if 0 <= x < image_width and 0 <= y < image_height:
        return image[y][x]
    else:
        return image[0][0]

def enhance_image(image):
    # Copying a 2D array isn't as simple as just image.copy(). That way you get a new list of pointers to the
    # existing rows. You have to make a new copy of each row
    new_image = list()
    for row in image:
        new_image.append(row.copy())

    # We addex spare space around the edge so let's use it to avoid having to check for out of bounds indices
    for y in range(0, image_height):
        for x in range(0, image_width):
            # Get the window of 3x3 pixels around the target pixel
            str1 = lookup_pixel(y-1, x-1) + lookup_pixel(y-1, x) + lookup_pixel(y-1,x+1)
            str2 = lookup_pixel(y, x-1) + lookup_pixel(y, x) + lookup_pixel(y,x+1)
            str3 = lookup_pixel(y+1, x-1) + lookup_pixel(y+1, x) + lookup_pixel(y+1,x+1)
            pixel_window = str1 + str2 + str3

            # Use the 3x3 pixel window to lookup the replacement character for the new image and set it
            iea_index = binary_string_to_decimal(pixels_to_binary(pixel_window))
            new_image[y][x] = iea[iea_index]

    return new_image

# Return the number of lit pixels in the image - used for part 1 & 2 solution
def count_lit_pixels(image):
    count_lit_pixels = 0
    for row in image:
        count_lit_pixels += row.count("#")
    return count_lit_pixels


# ---------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN ----------------------------------------------
# ---------------------------------------------------------------------------------------------

# Extra space around edge of image
extra_image_space = 10

# Image Enhancement Algorithm
iea = ""

# Image
image = list()
image_width, image_height = 0, 0

# Start by loading the input data - includes the IEA and the image grid
load_input_data()

# Display the image for testing
display_image(image, -1, -1)

for i in range(0, 2):
    image = enhance_image(image)
    display_image(image, -1, -1)

    # Detect if the growth of the image has hit the edge of our grid. 
    # If so then we need a bigger extra_image_space
    if(i%2 == 1):
        if(image[1].count("#") > 0):
            print(f"Iteration {i}: HIT EDGE")
        else:
            print(f"Iteration {i}")

print("Solution: ", count_lit_pixels(image))