from PIL import Image
def convert_message_to_binary_list(message):
  binary_list=[]
  for character in message:
    binary_list.append(format(ord(character), '08b'))
  return binary_list
def convert_integer_to_binary(color_value):
  return format(color_value, '08b')
def convert_to_integer_from_binary(binary_string):
    return int(binary_string,2)
def change_least_significant_bit(color_binary, lsb):
    binary_list=list(color_binary)
    binary_list[-1]=lsb
    return ''.join(binary_list)
def change_pixels_colors_least_significant_bits(binary_message, pixel_list, continue_bit):
  binary_message_index=0
  for pixel_index in range (len(pixel_list)):
    new_colors = []
    for color_value in pixel_list[pixel_index]:
      color_binary = convert_integer_to_binary(color_value)
      if binary_message_index ==8:
          if continue_bit=='1':
              new_colors.append(convert_to_integer_from_binary(change_least_significant_bit(color_binary, '1')))
          else:
              new_colors.append(convert_to_integer_from_binary(change_least_significant_bit(color_binary, '0')))
      else:
          new_colors.append(convert_to_integer_from_binary(change_least_significant_bit(color_binary, binary_message[binary_message_index])))
      binary_message_index=binary_message_index+1
    pixel_list[pixel_index]=(new_colors[0], new_colors[1], new_colors[2])
  return pixel_list
def perform_lsb_steg(new_img, binary_list):
    pixels = new_img.getdata()
    pixel_index = 0
    GROUP_SIZE = 3
    for index in range(len(binary_list)):
        current_pixel_list = []
        i = 0
        for i in range(GROUP_SIZE):
            current_pixel_list.append(pixels[pixel_index + 1])
        new_pixels = []
        if index == len(binary_list) - 1:
            new_pixels = change_pixels_colors_least_significant_bits(binary_message=binary_list[index], pixel_list=current_pixel_list, continue_bit='1')
        else:
            new_pixels = change_pixels_colors_least_significant_bits(binary_message=binary_list[index], pixel_list=current_pixel_list, continue_bit='0')
        pixel_index= (i+1) + pixel_index
        yield(new_pixels)

def decrypt_character_from_pixel_group(pixel_list):
    binary_string=''
    continue_flag=''
    index=0
    for pixel in pixel_list:
        for color in pixel:
            color_list=list(convert_integer_to_binary(color))
            if index!=8:
                binary_string+=color_list[-1]
                index=index+1
            else:
                continue_flag=color_list[-1]
    character = chr(int(binary_string,2))
    return character, continue_flag

def decrypt_binary_string_from_pixel_group(pixel_list):
    binary_string=''
    continue_flag=''
    index=0
    for pixel in pixel_list:
        for color in pixel:
            color_list=list(convert_integer_to_binary(color))
            if index!=8:
                binary_string+=color_list[-1]
                index=index+1
            else:
                continue_flag=color_list[-1]

    return binary_string, continue_flag

def save_file(binary_string, output_file):
    try:
        if len(binary_string) %8 !=0:
            raise ValueError("Binary string lentgh must be a multiple of 8")
        byte_chunks=[]
        for i in range (0,len(binary_string), 8):
            byte_chunks.append(binary_string[i:i+8])
        byte_list=[]
        for byte_chunk in byte_chunks:
            byte_value=int(byte_chunk, 2)
            byte_list.append(byte_value)
        file_bytes=bytes(byte_list)
        with open (output_file, 'wb') as file:
            file.write(file_bytes)
    except Exception as e:
        print(f"An error occurred: {e}")
class ImageSteganography:
    def encrypt(input_file, message, output_file):
        binary_list= convert_message_to_binary_list(message)
        image = Image.open(input_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        width, height = image.size
        new_img=image.copy()
        current_pixel_x = 0
        current_pixel_y = 0
        for pixel_list in perform_lsb_steg(new_img=new_img, binary_list=binary_list):
            for pixel in pixel_list:
                new_img.putpixel((current_pixel_x, current_pixel_y), pixel)
                if current_pixel_x==width:
                    current_pixel_x=0
                    current_pixel_y=current_pixel_y+1
                else:
                    current_pixel_x=current_pixel_x+1
        new_img.save(output_file)

    def encrypt_file(input_file, hidden_file, output_file):
        binary_list= []
        with open (hidden_file,'rb') as hf:
            file_bytes=hf.read()
            for byte in file_bytes:
                binary_list.append(format(byte, '08b'))
        image = Image.open(input_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        width, height = image.size
        new_img=image.copy()
        current_pixel_x = 0
        current_pixel_y = 0
        for pixel_list in perform_lsb_steg(new_img=new_img, binary_list=binary_list):
            for pixel in pixel_list:
                new_img.putpixel((current_pixel_x, current_pixel_y), pixel)
                if current_pixel_x==width:
                    current_pixel_x=0
                    current_pixel_y=current_pixel_y+1
                else:
                    current_pixel_x=current_pixel_x+1
        new_img.save(output_file)

    def decrypt(input_file):
        image=Image.open(input_file)
        pixels=list(image.getdata())
        GROUP_SIZE=3
        message=''
        for index in range (0,len(pixels), GROUP_SIZE):
            character, continue_flag = decrypt_character_from_pixel_group(pixels[index:index+GROUP_SIZE])
            message=message + character
            if continue_flag =='1':
                break
        print(f"Decrypted Message: {message}")

    def decrypt_file(input_file, output_file):
        image=Image.open(input_file)
        pixels=list(image.getdata())
        GROUP_SIZE=3
        full_binary_string=''

        for index in range (0,len(pixels), GROUP_SIZE):
            binary_string, continue_flag = decrypt_binary_string_from_pixel_group(pixels[index:index+GROUP_SIZE])
            full_binary_string+=binary_string
            if continue_flag =='1':
                break
        save_file(binary_string=full_binary_string, output_file=output_file)
