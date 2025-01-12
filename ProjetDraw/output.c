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
    Cursor mycursor = createCursor();
    Cursor Cursor = createCursor();
    setPosition(&myCursor, 350, 300);
    setColor(&myCursor, (SDL_Color){0, 0, 255, 255});
    setPosition(&mycursor, 400, 300);
    setColor(&mycursor, (SDL_Color){255, 0, 0, 255});
    setPosition(&Cursor, 400, 300);
    setColor(&Cursor, (SDL_Color){0, 128, 0, 255});
    for (    float size = 10; size <= 200;     size += 20) {
    drawSquare(renderer, &myCursor, size);
    drawCircle(renderer, &myCursor, size);
    drawCircle(renderer, &Cursor, size);
    rotate(&mycursor, 45);
    drawArc(renderer, &mycursor, size, 90);

    }
    SDL_RenderPresent(renderer);
    SDL_Delay(3000);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}