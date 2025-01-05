#include <SDL2/SDL.h>
#include "../C/include/draw_cursor.h"

int main() {
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *window = SDL_CreateWindow("Draw++ Test", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    Cursor cursor = createCursor();
    setPosition(&cursor, 200, 150);
    setColor(&cursor, (SDL_Color){255, 0, 0, 255}); // Rouge
    drawCircle(renderer, &cursor, 50, 0);
    setPosition(&cursor, 50, 100);
    drawSquare(renderer, &cursor, 45, 1);
    setPosition(&cursor, 300, 60);
    drawRectangle(renderer,&cursor,15,80,1);
    setPosition(&cursor, 300, 60);
    drawTriangle(renderer,&cursor,30,50,0);

    SDL_RenderPresent(renderer);
    SDL_Delay(3000);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
