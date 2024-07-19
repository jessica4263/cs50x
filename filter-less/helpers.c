#include "helpers.h"
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

void swap(RGBTRIPLE *a, RGBTRIPLE *b);
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green and blue.
            BYTE red = image[i][j].rgbtRed;
            BYTE green = image[i][j].rgbtGreen;
            BYTE blue = image[i][j].rgbtBlue;

            int average = round((red + green + blue) / 3.0);
            // Update pixel values.
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green and blue.
            BYTE red = image[i][j].rgbtRed;
            BYTE green = image[i][j].rgbtGreen;
            BYTE blue = image[i][j].rgbtBlue;
            // Red
            int sepia_red = round(.393 * red + .769 * green + .189 * blue);
            if (sepia_red > 255)
            {
                sepia_red = 255;
            }
            else if (sepia_red < 0)
            {
                sepia_red = 0;
            }
            // Green
            int sepia_green = round(.349 * red + .686 * green + .168 * blue);
            if (sepia_green > 255)
            {
                sepia_green = 255;
            }
            else if (sepia_green < 0)
            {
                sepia_green = 0;
            }
            // Blue
            int sepia_blue = round(.272 * red + .534 * green + .131 * blue);
            if (sepia_blue > 255)
            {
                sepia_blue = 255;
            }
            else if (sepia_blue < 0)
            {
                sepia_blue = 0;
            }
            // Update pixel values.
            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap
            swap(&image[i][j], &image[i][width - j - 1]);
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int copy_red = image[i][j].rgbtRed;
            int copy_green = image[i][j].rgbtGreen;
            int copy_blue = image[i][j].rgbtBlue;
            float average = 1;
            // Right pixel
            if (j + 1 < width)
            {
                copy_red += image[i][j + 1].rgbtRed;
                copy_green += image[i][j + 1].rgbtGreen;
                copy_blue += image[i][j + 1].rgbtBlue;
                average++;
                // Right upper pixel
                if (i - 1 >= 0)
                {
                    copy_red += image[i - 1][j + 1].rgbtRed;
                    copy_green += image[i - 1][j + 1].rgbtGreen;
                    copy_blue += image[i - 1][j + 1].rgbtBlue;
                    average++;
                }
            }
            // Left Pixel
            if (j - 1 >= 0)
            {
                copy_red += image[i][j - 1].rgbtRed;
                copy_green += image[i][j - 1].rgbtGreen;
                copy_blue += image[i][j - 1].rgbtBlue;
                average++;
                // Left upper pixel
                if (i - 1 >= 0)
                {
                    copy_red += image[i - 1][j - 1].rgbtRed;
                    copy_green += image[i - 1][j - 1].rgbtGreen;
                    copy_blue += image[i - 1][j - 1].rgbtBlue;
                    average++;
                }
            }
            // Lower pixel
            if (i + 1 < height)
            {
                copy_red += image[i + 1][j].rgbtRed;
                copy_green += image[i + 1][j].rgbtGreen;
                copy_blue += image[i + 1][j].rgbtBlue;
                average++;
                // Right lower pixel
                if (j + 1 < width)
                {
                    copy_red += image[i + 1][j + 1].rgbtRed;
                    copy_green += image[i + 1][j + 1].rgbtGreen;
                    copy_blue += image[i + 1][j + 1].rgbtBlue;
                    average++;
                }
                // Left lower pixel
                if (j - 1 >= 0)
                {
                    copy_red += image[i + 1][j - 1].rgbtRed;
                    copy_green += image[i + 1][j - 1].rgbtGreen;
                    copy_blue += image[i + 1][j - 1].rgbtBlue;
                    average++;
                }
            }
            // Upper pixel
            if (i - 1 >= 0)
            {
                copy_red += image[i - 1][j].rgbtRed;
                copy_green += image[i - 1][j].rgbtGreen;
                copy_blue += image[i - 1][j].rgbtBlue;
                average++;
            }
            copy[i][j].rgbtRed = round(copy_red / average);
            copy[i][j].rgbtGreen = round(copy_green / average);
            copy[i][j].rgbtBlue = round(copy_blue / average);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}
void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}
