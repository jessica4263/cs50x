#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int P[] = { 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int compute_score(string p);
int main (void)
{
    string p1 = get_string("Player 1: ");
    string p2 = get_string("Player 2: ");
    //scores
    int value1= compute_score(p1);
    int value2= compute_score(p2);
    //print winner
    if (value1 > value2)
    {
        printf("Player 1 wins!\n");
    }
    else if (value1 < value2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
    //compute score
int compute_score(string p)
{
    int value = 0;
    for (int i = 0, len = strlen(p); i < len; i++)
    {
        if(isupper(p[i]))
        {
            value += P[p[i]-'A'];
        }
        else if (islower(p[i]))
        {
            value += P[p[i]-'a'];
        }
    }
    return value;
}
