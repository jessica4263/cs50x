#include <stdio.h>

int main(void)
{
    printf("Hello, world\n");
}
    char'A'= 1, 'B'= 3, 'C'= 3,'D'= 2,'E'= 1,'F'= 4,'G'= 2,'H'= 4,'I'= 1,'J'= 8,'K'= 5,
    'L'= 1,'M'= 3,'N'= 1,'O'= 1,'P'= 3,'Q'= 10,'R'= 1,'S'= 1,'T'= 1,'U'= 1,'V'= 4,'W'= 4,
    'X'= 8,'Y'= 4,'Z'= 10;

    char letters[26] = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
    int value[26] = { 1, 3, 3, 2, 1, 4, 2 ,4 ,1 , 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    string p1 = get_string("Player 1: ");
    for (int i = 0, n = strlen(p1); i < n; i++)
    printf ("%c", toupper (p1[i]));
    printf ("\n");
    string p2 = get_string("Player 2: ");
    for (int i = 0, n = strlen(p2); i < n; i++)
    printf ("%c", toupper (p2[i]));
    printf ("\n");

    string player[N];
    for (int i = 0, c = 1; i < N; i++, c++)
    {
        player[i] = get_string("Player %i: ",c);
        int n = strlen(player[i]);
        if (islower (player[i]))
        {
            int toupper(player[i]);
        }
        for (int j = 0; j < n; j++)
        if (islower (player[i][j]))
        {
            char toupper(player[i][j]);
            printf ("%i", player[i][j]);
        }
            printf ("\n");
    }
}
}
string cyphert(string pt)
{
    string ct = 0;
    for (int i = 0, len = strlen(pt); i < len; i++)
    {
        if (isalpha(pt[i]))
        {
            ct[i] = (pt[i] + key) % 26;
        }
        else
        {
            continue;
        }
    }
    return string;
}
// Formula
// c[i] = (p[i] + key) % 26
