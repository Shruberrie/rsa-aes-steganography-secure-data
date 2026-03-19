import argparse
from stegclasses.metadata import PDFFileMetadata
from stegclasses.imagesteg import ImageSteganography
def encrypt(type, input_file, metadat_name, message, output_file, parser, hidden_file):
    if type=="pdf":
        if metadat_name and message:
            PDFFileMetadata.encrypt(file_path=input_file,metadata_key_name= metadat_name, output_file_path=output_file, message=message)
        else:
            PDFFileMetadata.encrypt_file(file_path=input_file, output_file_path=output_file, metadata_key_name=metadat_name, hidden_file=hidden_file)

    elif type == "image":
        if hidden_file:
            ImageSteganography.encrypt_file(input_file=input_file, hidden_file=hidden_file, output_file=output_file)
        else:
            ImageSteganography.encrypt(input_file=input_file, message=message, output_file=output_file)

    else:
        parser.errpr("The only types acceptable are pdf and image")
def decrypt(type, input_file, parser, output_file, metadata_name):
    if type=="pdf":
        if output_file:
            PDFFileMetadata.decrypt_file(input_file_path=input_file,output_file_path=output_file, metadata_key_name=metadata_name)
        else:

            PDFFileMetadata.decrypt(file_path=input_file)
    elif type == "image":
        if output_file:
            ImageSteganography.decrypt_file(input_file=input_file, output_file=output_file)
        else:
            ImageSteganography.decrypt(input_file=input_file)
    else:
        parser.error("The only types acceptable are pdf and image")
def main():
    parser=argparse.ArgumentParser(description="Script that performs steganography on PDFs, images and audio files")
    parser.add_argument("-d", action="store_true", help="Option decrypt")
    parser.add_argument("-e", action="store_true",  help="Option encrypt")
    parser.add_argument("-t", required=True, help="The type of file that steganography will be performed on")
    parser.add_argument("-f", required=True, type=str, help="Input file path")
    parser.add_argument("-o", required=False, type=str, help="Output file path")
    parser.add_argument("-m", required=False, type=str, help="The message you want to hide")
    parser.add_argument("-mn", required=False, type=str, help="The metadata key name. This must start with a /")
    parser.add_argument("-hf", required=False, type=str, help="The file path for the file you want to hide")

    args = parser.parse_args()
    if not (args.d or args.e):
        parser.error("The script requires either a -d or -e flag")
    if args.d:
        decrypt(type=args.t, input_file=args.f, parser=parser, output_file=args.o, metadata_name=args.mn)
    elif args.e:
        if args.o and (args.m or args.hf):
            encrypt(type=args.t, input_file=args.f, metadat_name=args.mn, message=args.m, output_file=args.o, parser=parser, hidden_file=args.hf)
        else:
            parser.error("The script requires the -o and (-m or -hf) flag for the encrypt function")

if __name__== "__main__":
    main()



