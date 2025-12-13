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

    try:
        f = open(input_img, 'rb')
        imageData = list(f.read()) #The contents of the image
        f.close()
    except FileNotFoundError:
        print("File entered does not exsist.")
        return
    
    bits = int.from_bytes(imageData[28:30], byteorder='little') #bits per pixel
    bytes = bits // 8 #bytes per pixel
    header = int.from_bytes(imageData[10 : 14], byteorder='little') #stores the length of the header of the BMP image

    if bytes < 3:
        print("This image is not supported (must be either 24 or 32 bit image)")


    messageBytes = message.encode('utf-8') #Convert the message using utf-8 encoding to bytes
    messageBits = [] #empty list used to store the bits 

    #converting each byte into 8 bits 
    for byte in messageBytes: 
        binary_string = format(byte, '08b') #this line converts the bytes into an 8 bit string using '08b' ensures that even empty spaces are filed with 0s
        for bit in binary_string: 
            messageBits.append(int(bit)) #here I convert the zeros and ones to inegers and stores them in the messageBits array

    for i in range(8):
        messageBits.append(0) #appends 8 zeros at the end message_bits to signal the end of the message (Delimiter)


    pixels = (len(imageData) - header) // bytes #calculates total pixels in the image
    freeBits = pixels * 3 #free space availble but this considers that each pixel contains 3 channels RGB (Alpha is skipped as it might affect the image greatly)
    if len(messageBits) > freeBits: 
        print("This message is too big for the image.")
        print(f"Available bits: {freeBits}, \n required: {len(messageBits)}")
        return

    currBit = 0
    currPixel = header # this stores the current pixel being edited starting after the byte_offset which is the header

    while currBit < len(messageBits):
        for channel in range(3): #loop through each channel (RGB)
            if currBit >= len(messageBits):
                break

            imageData[currPixel + channel] = (imageData[currPixel + channel] & 0xFE) | messageBits[currBit] 
            #the line above CLEARS the LSB and replaces with the current message bit by using an 'AND' and an 'OR' logic gates
            currBit += 1 #move to the next bit in the RGB

        currPixel += bytes #after we go through each channel and embed our message bit, we add 'bytes' to 'currPixel' to move to the next pixel in line
    

    try:
        file = open(output_img, 'wb')
        file.write(bytes(imageData)) #implements all of what we did in the new output file
        print(f"You're message has been sucessfully hidden in {output_img}.")
    except:
        print("Error when writing to output image, please check file path permissions.")
     

###########################################################################################################################################################################

def Decoder(fileName):
    try:
        f = open(fileName, 'rb')
        imageData = f.read()
    except FileNotFoundError:
        print("File does not exsit")

    bits = int.from_bytes(imageData[28:30], byteorder='little')
    bytes = bits // 8
    header = int.from_bytes(imageData[10:14], byteorder='little')
    bitString = []


    currPixel = header #keeps track of the pixel currently on, this is set to bytes_offset so that it starts exactly at the beggining of the pixel data 

    #obtaining the bits that are stored in the LSB of ONLY the RGB channels
    while currPixel < len(imageData):
        for channel in range(3):
            if currPixel + channel >= len(imageData):
                break
            bitString.append(imageData[currPixel + channel] & 1) #this line gets the binary number of each channel and uses an AND gate to get the LSB (& 1)
            if len(bitString) >= 8 and bitString[-8:] == [0]*8: #detectes the delimiter added so that it stops looping through the pixels if reached (smart pixel looping)
                currPixel = len(imageData) 
                break
        currPixel += bytes


    # Converting the bits to bytes
    message_bytes = []
    for i in range(0, len(bitString), 8):
        byte = bitString[i:i+8] #slices the bits so that they are groups of 8, creating 1 byte
        if len(byte) < 8:
            break
        byte_value = int(''.join(str(b) for b in byte), 2) #this converts the 8 bits into an intger which is why we wrote the '2'
        if byte_value == 0:  #We have reached delimiter so terminate loop
            break
        message_bytes.append(byte_value) #append the current byte value to the message_byte list

    #converting the bytes to characters and letters to retrive the secret message
    message = bytes(message_bytes).decode('utf-8', errors='ignore')
    return message

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
            
        elif choice == '2':
            input_file = input("Enter BMP file to decode: ")
            message = Decoder(input_file)
            print(f"hidden message: {message}")

        elif choice == '3':
            print("Exiting program...")
            print("Thank You, goodbye.")
            break
     

###########################################################################################################################################################################

if __name__ == "__main__":
    mainMenu()
