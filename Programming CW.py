###########################################################################################################################################################################

def Encoder(input_img, output_img):
    try:
        choice = int(input("Do you want to type a message(1) or enter a .txt file(2):")) #Duel input method
    except ValueError:
        print("Must input numeric value") 
        return
    
    message = ""

    if choice == 1: message = input("Enter you're secret message:")

    elif choice == 2:
        file_name = input("Enter file name or path containing the secret message:")
        try:
            file = open(file_name, 'r')
            message = file.read()
            file.close()
        except FileNotFoundError:
            print("This .txt file does not exsist")
            return
    else:
        print("Invalid input, must enter either 1 or 2")
        return

    if not input_img.lower().endswith(".bmp"): #if the user enters and image that is not of type BMP
        print("Only BMP image type is supported.") 
        return 
    
    if message.strip() == "": 
        print("Can not accept empty string.") 
        return

    f = open(input_img, 'rb')
    imageData = list(f.read()) #The contents of the image
    f.close()
  
     

###########################################################################################################################################################################

def Decoder(fileName):
    pass

###########################################################################################################################################################################

def mainMenu():
    while True:
        print(" \n __________Steganography Menu__________")
        print("1. hide a message in an image")
        print("2. Decode message from an image")
        print("3. Exit program")
        choice = input("Choose an option: ")

        if choice == '1':
            input_file = input("Enter BMP file to hide message in: ")
            output_file = input("Enter output file name: ")

            if output_file.strip() == "":
                output_file = "mod.bmp"
            
            Encoder(input_file, output_file)

        elif choice == '3':
            print("Exiting program...")
            print("Thank You, goodbye.")
            break
     

###########################################################################################################################################################################

if __name__ == "__main__":
    mainMenu()
