# BMP2ASM
Extracts palettes and tilesets from bitmap images and converts to 68k assembly code for the sega genesis.

## How To Use

### Extracting Palettes
![Screenshot 2025-04-11 211355](https://github.com/user-attachments/assets/2b2f7099-ae47-4286-aeae-fa21a5fa087c)

When on this screen (should appear right after running python file), type **1** and press **enter**.

![Screenshot 2025-04-11 211637](https://github.com/user-attachments/assets/6233f401-21cc-42e9-855d-64e6c4df602a)

You should then appear on this screen, type **the filepath of your bitmap image** and then press **enter**.

![Screenshot 2025-04-11 211551](https://github.com/user-attachments/assets/b5f739d2-f104-43c7-9865-023368f0a6db)

Afterword you will be on this screen. The "name" refers to what the label identifying your palette's address and the metadata (configurable in settings.ini) automatically generated for your palette will be named. Type **the name you would like to use** and press **enter**.

![Screenshot 2025-04-11 211619](https://github.com/user-attachments/assets/383b08bc-8930-4d0e-b417-26470927c25a)

Now you can choose where to save your file and what it will be named. If you type **1** and press **enter**, you can use the automatically generated file location based on the source address and name. Or, you can also type **your own specific path** and press **enter**.
> [!WARNING]
> Note: If any other file already exists in the directory you are saving it to with the same name ***IT WILL BE PERMANENTLY ERASED***.
> Also, when manually selecting an address, make sure it includes *.asm* at the end of the file name.

You have now exported a palette from a bitmap image and converted it into assembly code!

### Extracting Tiles
![Screenshot 2025-04-11 211355](https://github.com/user-attachments/assets/2b2f7099-ae47-4286-aeae-fa21a5fa087c)

Follow the exact same steps from the [Extracting Palettes](#extracting-palettes) section, howver when you get to this screen (the first screen) type **2** instead of **1**.

You have now exported a tileset from a bitmap image and converted it into assembly code!

### Configuring BMP2ASM
BMP2ASM uses *settings.ini* for configuration. Some things it can do include:
- Adding metadata for where you want to place your palette in *CRAM*. (pal_dest)
- Adding metadata for where you want to place your tileset in *VRAM*. (tile_dest)
- Adding metadta to count the amount of tiles in the set. (num_tiles)

Each of the options creates a constant to set certain values for metadata. To change any of these options simply replace the true with false and vice versa after the "=".

Bitmap to 68K Assembly Converter
Written by Kreglar (Miles Cooper 2025)
Version 4/11/25
