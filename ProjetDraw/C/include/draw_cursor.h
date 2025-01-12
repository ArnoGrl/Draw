#ifndef DRAW_CURSOR_H
#define DRAW_CURSOR_H

#include <SDL2/SDL.h>
#include <math.h>

// Defines the Cursor structure to track position, color, thickness, and angle
typedef struct {
    int x, y;                   // Cursor position on screen
    SDL_Color color;            // Drawing color
    int thickness;              // Line thickness
    double angle;               // Cursor angle in degrees
} Cursor;

// Cursor management functions
Cursor createCursor();                              // Initializes a new cursor
void setPosition(Cursor *cursor, int x, int y);    // Updates cursor position
void setColor(Cursor *cursor, SDL_Color color);    // Sets cursor drawing color
void setThickness(Cursor *cursor, int thickness); // Sets line thickness
void rotate(Cursor *cursor, double angle);        // Rotates the cursor

// Drawing functions
void drawSquare(SDL_Renderer *renderer, Cursor *cursor, int size);    // Draws a square
void drawTriangle(SDL_Renderer *renderer, Cursor *cursor, int base, int height); // Draws a triangle
void drawRectangle(SDL_Renderer *renderer, Cursor *cursor, int width, int height); // Draws a rectangle
void drawCircle(SDL_Renderer *renderer, Cursor *cursor, int radius);  // Draws a circle
void drawLine(SDL_Renderer *renderer, Cursor *cursor, int length);    // Draws a straight line
void drawPoint(SDL_Renderer *renderer, Cursor *cursor);               // Draws a single point
void drawArc(SDL_Renderer *renderer, Cursor *cursor, int radius, double angle); // Draws an arc

#endif // DRAW_CURSOR_H