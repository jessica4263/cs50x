#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Change owed: ");
    }
    while (n < 1);
    int q = 25, di = 10, ni = 5, p = 1;
    int c1 = n / q;
    int res1 = n - (c1 * q);
    int c2 = res1 / di;
    int res2 = res1 - (c2 * di);
    int c3 = res2 / ni;
    int res3 = res2 - (c3 * ni);
    int c4 = res3 / p;
    {
        printf("%d\n", c1 + c2 + c3 + c4);
    }
}
