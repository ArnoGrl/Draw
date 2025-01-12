#ifndef DRAW_CURSOR_H
#define DRAW_CURSOR_H

#include <SDL2/SDL.h>
#include <math.h>

// Structure du curseur
typedef struct {
    int x, y;                   // Position
    SDL_Color color;            // Couleur
    int thickness;              // Épaisseur
    double angle;               // Angle en degrés
} Cursor;

// Fonctions de gestion du curseur
Cursor createCursor();
void setPosition(Cursor *cursor, int x, int y);
void setColor(Cursor *cursor, SDL_Color color);
void setThickness(Cursor *cursor, int thickness);
void rotate(Cursor *cursor, double angle);

// Fonctions de dessin
void drawSquare(SDL_Renderer *renderer, Cursor *cursor, int size);
void drawTriangle(SDL_Renderer *renderer, Cursor *cursor, int base, int height);
void drawRectangle(SDL_Renderer *renderer, Cursor *cursor, int width, int height);
void drawCircle(SDL_Renderer *renderer, Cursor *cursor, int radius);
void drawLine(SDL_Renderer *renderer, Cursor *cursor, int length);
void drawPoint(SDL_Renderer *renderer, Cursor *cursor);
void drawArc(SDL_Renderer *renderer, Cursor *cursor, int radius, double angle);

#endif // DRAW_CURSOR_H