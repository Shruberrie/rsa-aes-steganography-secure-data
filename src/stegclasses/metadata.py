import PyPDF2
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
class PDFFileMetadata:
    def decrypt(file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata
            for key in metadata:
                print(f"{key}:{metadata[key]}")
    def encrypt(file_path, metadata_key_name, message, output_file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            writer.append_pages_from_reader(reader)
            metadata = reader.metadata
            metadata.update({metadata_key_name: message})
            writer.add_metadata(metadata)

            with open(output_file_path, 'wb') as output_file:
                writer.write(output_file)
            print("Message hidden successfully")

    def encrypt_file(file_path,metadata_key_name, hidden_file, output_file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            writer.append_pages_from_reader(reader)
            binary_list=[]
            with open(hidden_file, 'rb') as hf:
                file_bytes=hf.read()
                for byte in file_bytes:
                    binary_list.append(format(byte, '08b'))
            message = ''.join(binary_list)
            metadata = reader.metadata
            metadata.update({metadata_key_name: message})
            writer.add_metadata(metadata)
            with open(output_file_path, 'wb') as output_file:
                writer.write(output_file)
            print("Message hidden successfully")
    def decrypt_file(input_file_path, output_file_path, metadata_key_name):
        with open (input_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata=reader.metadata
            found_flag=False
            for item in metadata:
                if item == metadata_key_name:
                    found_flag=True
                    save_file(binary_string=metadata[item], output_file=output_file_path)
            if found_flag==False:
                print("Sorry the metadata key name was not found")

