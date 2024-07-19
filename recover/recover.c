#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512
int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        return 2;
    }
    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];
    // While there's still data left to read from the memory card
    char filenames[8];
    int image_number = 0;
    FILE *img = NULL;
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                fclose(img);
                image_number++;
            }
            sprintf(filenames, "%03i.jpg", image_number);
            img = fopen(filenames, "w");
            if (img == NULL)
            {
                return 3;
            }
        }
        if (img != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }
    if (img != NULL)
    {
        fclose(img);
        fclose(card);
    }
    
}
