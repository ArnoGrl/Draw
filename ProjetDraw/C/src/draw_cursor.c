#include <SDL2/SDL.h>
#include <math.h>
#include "../include/M_PI.h"
#include "../include/draw_cursor.h"

// Créer un curseur
Cursor createCursor() {
    Cursor cursor;
    cursor.x = 0;
    cursor.y = 0;
    cursor.color = (SDL_Color){0, 0, 0, 255}; // Noir par défaut
    cursor.thickness = 1;                     // Épaisseur par défaut
    cursor.angle = 0.0;                       // Angle initial
    return cursor;
}

// Définir la position du curseur
void setPosition(Cursor *cursor, int x, int y) {
    cursor->x = x;
    cursor->y = y;
}

// Définir la couleur du curseur
void setColor(Cursor *cursor, SDL_Color color) {
    cursor->color = color;
}

// Définir l'épaisseur du trait
void setThickness(Cursor *cursor, int thickness) {
    cursor->thickness = thickness;
}

// Faire pivoter le curseur
void rotate(Cursor *cursor, double angle) {
    cursor->angle += angle;
    // Maintenir l'angle entre 0 et 360 degrés
    cursor->angle = fmod(cursor->angle, 360.0);
}

// Dessiner un carré (contour uniquement)
void drawSquare(SDL_Renderer *renderer, Cursor *cursor, int size) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_Rect rect = {cursor->x, cursor->y, size, size};

    // Dessiner uniquement le contour
    SDL_RenderDrawRect(renderer, &rect);
}

// Dessiner un rectangle (contour uniquement)
void drawRectangle(SDL_Renderer *renderer, Cursor *cursor, int width, int height) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_Rect rect = {cursor->x, cursor->y, width, height};

    // Dessiner uniquement le contour
    SDL_RenderDrawRect(renderer, &rect);
}

// Dessiner un triangle (contour uniquement)
void drawTriangle(SDL_Renderer *renderer, Cursor *cursor, int base, int height) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

    // Calculer les sommets du triangle
    int x1 = cursor->x;
    int y1 = cursor->y;

    int x2 = cursor->x + base;
    int y2 = cursor->y;

    int x3 = cursor->x + (base / 2);
    int y3 = cursor->y - height;

    // Dessiner uniquement les contours du triangle
    SDL_RenderDrawLine(renderer, x1, y1, x2, y2); // Base
    SDL_RenderDrawLine(renderer, x1, y1, x3, y3); // Côté gauche
    SDL_RenderDrawLine(renderer, x2, y2, x3, y3); // Côté droit
}

// Dessiner un cercle (contour uniquement)
void drawCircle(SDL_Renderer *renderer, Cursor *cursor, int radius) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

    // Dessiner uniquement le contour
    for (double angle = 0; angle < 360; angle += 0.1) {
        int x = cursor->x + (int)(cos(angle * M_PI / 180.0) * radius);
        int y = cursor->y + (int)(sin(angle * M_PI / 180.0) * radius);
        SDL_RenderDrawPoint(renderer, x, y);
    }
}

// Dessiner une ligne
void drawLine(SDL_Renderer *renderer, Cursor *cursor, int length) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    int endX = cursor->x + (int)(cos(cursor->angle * M_PI / 180.0) * length);
    int endY = cursor->y + (int)(sin(cursor->angle * M_PI / 180.0) * length);
    SDL_RenderDrawLine(renderer, cursor->x, cursor->y, endX, endY);
}

// Dessiner un point
void drawPoint(SDL_Renderer *renderer, Cursor *cursor) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_RenderDrawPoint(renderer, cursor->x, cursor->y);
}

// Dessiner un arc de cercle
void drawArc(SDL_Renderer *renderer, Cursor *cursor, int radius, double angle) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    double startAngle = cursor->angle;
    double endAngle = cursor->angle + angle;

    for (double a = startAngle; a <= endAngle; a += 1.0) {
        int x = cursor->x + (int)(cos(a * M_PI / 180.0) * radius);
        int y = cursor->y + (int)(sin(a * M_PI / 180.0) * radius);
        SDL_RenderDrawPoint(renderer, x, y);
    }
}