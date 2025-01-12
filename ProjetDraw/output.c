#include <stdio.h>
#include <stdbool.h>
#include "C/include/draw_cursor.h"
#include "C/src/draw_cursor.c"
#include <SDL2/SDL.h>

int main() { 
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *window = SDL_CreateWindow("Draw++ Test", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    Cursor myCursor = createCursor();
    Cursor Cursor = createCursor();
    float i = 0;
    float j = 50;
    float g = 100;
    float a = 25;
    float b = 50;
    while (i < 100) {
    setPosition(&myCursor, j, g);
    setPosition(&Cursor, a, b);
    j += 5;
    g += 2;
    a += 3;
    b += 8;
    setColor(&myCursor, (SDL_Color){255, 0, 0, 255});
    setColor(&Cursor, (SDL_Color){0, 0, 255, 255});
    drawLine(renderer, &myCursor, 10);
    rotate(&myCursor, 90);
    drawPoint(renderer, &myCursor);
    drawArc(renderer, &myCursor, 50, 90);
    drawCircle(renderer, &myCursor, 50);
    drawSquare(renderer, &myCursor, 50);
    drawLine(renderer, &Cursor, 10);
    rotate(&Cursor, 90);
    drawPoint(renderer, &Cursor);
    drawArc(renderer, &Cursor, 50, 90);
    drawCircle(renderer, &Cursor, 50);
    drawSquare(renderer, &Cursor, 50);
    i++;

    }
SDL_RenderPresent(renderer);
SDL_Delay(3000);
SDL_DestroyRenderer(renderer);
SDL_DestroyWindow(window);
SDL_Quit();
    return 0;
}