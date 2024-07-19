#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int lower[26] = {97,  98,  99,  100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122};
int upper[26] = {65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
                 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90};
int plain(string p);
// Get Key
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar Key\n");
        return 1;
    }
    else if (argc == 2)
    {
        for (int i = 0, j = 1, len = strlen(argv[1]); i < len; i++, j++)
            if (isalpha(argv[1][i]))
            {
                printf("Usage: ./caesar Key\n");
                return 1;
            }
            else if (argv[1][i] == '-')
            {
                printf("Usage: ./caesar Key\n");
                return 1;
            }
            else if (j == len)
            {
                string plaintext = get_string("plaintext: ");
                int key = atoi(argv[1]);
                for (int pt = 0, a = 0, l = strlen(plaintext); pt < l; pt++, a++)
                    if (isalpha(plaintext[pt]))
                    {
                        if (isupper(plaintext[pt]))
                        {
                            int p = plaintext[pt] - 'A';
                            int rotate = (p + key) % 26;
                            char cipher = upper[rotate];
                            if (a == 0)
                            {
                                printf("ciphertext: %c", cipher);
                            }
                            else
                            {
                                printf("%c", cipher);
                            }
                        }
                        else if (islower(plaintext[pt]))
                        {
                            int p = plaintext[pt] - 'a';
                            int rotate = (p + key) % 26;
                            char cipher = lower[rotate];
                            if (a == 0)
                            {
                                printf("ciphertext: %c", cipher);
                            }
                            else
                            {
                                printf("%c", cipher);
                            }
                        }
                    }
                    else
                    {
                        printf("%c", plaintext[pt]);
                    }
                printf("\n");
            }
            else
            {
                j++;
            }
    }
}
