#include <SDL2/SDL.h>
#include <math.h>
#include "../include/M_PI.h"
#include "../include/draw_cursor.h"

// Create a cursor with default properties
Cursor createCursor() {
    Cursor cursor;
    cursor.x = 0;
    cursor.y = 0;
    cursor.color = (SDL_Color){0, 0, 0, 255}; // Default color: black
    cursor.thickness = 1;                     // Default thickness: 1
    cursor.angle = 0.0;                       // Initial angle: 0 degrees
    return cursor;
}

// Set the cursor's position
void setPosition(Cursor *cursor, int x, int y) {
    cursor->x = x;
    cursor->y = y;
}

// Set the cursor's drawing color
void setColor(Cursor *cursor, SDL_Color color) {
    cursor->color = color;
}

// Set the line thickness for the cursor
void setThickness(Cursor *cursor, int thickness) {
    cursor->thickness = thickness;
}

// Rotate the cursor by a specified angle
void rotate(Cursor *cursor, double angle) {
    cursor->angle += angle;
    cursor->angle = fmod(cursor->angle, 360.0); // Keep angle between 0 and 360 degrees
}

// Draw a square (only the outline)
void drawSquare(SDL_Renderer *renderer, Cursor *cursor, int size) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_Rect rect = {cursor->x, cursor->y, size, size};
    SDL_RenderDrawRect(renderer, &rect); // Draw the square outline
}

// Draw a rectangle (only the outline)
void drawRectangle(SDL_Renderer *renderer, Cursor *cursor, int width, int height) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_Rect rect = {cursor->x, cursor->y, width, height};
    SDL_RenderDrawRect(renderer, &rect); // Draw the rectangle outline
}

// Draw a triangle (only the outline)
void drawTriangle(SDL_Renderer *renderer, Cursor *cursor, int base, int height) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

    // Calculate triangle vertices
    int x1 = cursor->x, y1 = cursor->y;
    int x2 = cursor->x + base, y2 = cursor->y;
    int x3 = cursor->x + (base / 2), y3 = cursor->y - height;

    // Draw triangle edges
    SDL_RenderDrawLine(renderer, x1, y1, x2, y2); // Base
    SDL_RenderDrawLine(renderer, x1, y1, x3, y3); // Left side
    SDL_RenderDrawLine(renderer, x2, y2, x3, y3); // Right side
}

// Draw a circle (only the outline)
void drawCircle(SDL_Renderer *renderer, Cursor *cursor, int radius) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

    // Draw circle outline using points
    for (double angle = 0; angle < 360; angle += 0.1) {
        int x = cursor->x + (int)(cos(angle * M_PI / 180.0) * radius);
        int y = cursor->y + (int)(sin(angle * M_PI / 180.0) * radius);
        SDL_RenderDrawPoint(renderer, x, y);
    }
}

// Draw a straight line from the cursor
void drawLine(SDL_Renderer *renderer, Cursor *cursor, int length) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    int endX = cursor->x + (int)(cos(cursor->angle * M_PI / 180.0) * length);
    int endY = cursor->y + (int)(sin(cursor->angle * M_PI / 180.0) * length);
    SDL_RenderDrawLine(renderer, cursor->x, cursor->y, endX, endY);
}

// Draw a point at the cursor's position
void drawPoint(SDL_Renderer *renderer, Cursor *cursor) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_RenderDrawPoint(renderer, cursor->x, cursor->y);
}

// Draw an arc from the cursor's position
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
