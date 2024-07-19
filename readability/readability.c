#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int letter(string t);
int word(string t);
int sentence(string t);
int main(void)
{
    string text = get_string("Text\n");
    double l = letter(text);
    double w = word(text);
    double s = sentence(text);
    double L = (l / w) * 100.0;
    double S = (s / w) * 100.0;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);
    if (grade > 1 && grade < 16)
    {
        printf("Grade %i\n", grade);
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
}
int letter(string t)
{
    int count = 0;
    for (int i = 0, len = strlen(t); i < len; i++)
    {
        if (isalpha(t[i]))
        {
            count++;
        }
    }
    return count;
}
int word(string t)
{
    int count = 0;
    for (int i = 0, len = strlen(t); i < len; i++)
    {
        if (isblank(t[i]))
        {
            count++;
        }
    }
    return count + 1;
}
int sentence(string t)
{
    int count = 0;
    for (int i = 0, len = strlen(t); i < len; i++)
    {
        if (ispunct(t[i]))
        {
            if (t[i] == 39 || t[i] == 34 || t[i] == 58 || t[i] == 59 || t[i] == 45 || t[i] == 44)
            {
                continue;
            }
            else
            {
                count++;
            }
        }
    }
    return count;
}
