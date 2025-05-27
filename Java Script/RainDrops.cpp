#include <graphics.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>

#define MAX_RAINDROPS 100

struct Raindrop {
    int x, y;
    int length;
    int speed;
}; 

void initializeRaindrops(Raindrop drops[], int count) {
    for (int i = 0; i < count; i++) {
        drops[i].x = rand() % getmaxx();
        drops[i].y = rand() % getmaxy();
        drops[i].length = 5 + rand() % 10;
        drops[i].speed = 1 + rand() % 5;
    }
}

void drawRaindrop(Raindrop drop) {
    setcolor(WHITE);
    line(drop.x, drop.y, drop.x, drop.y + drop.length);
}

void updateRaindrop(Raindrop &drop) {
    drop.y += drop.speed;
    if (drop.y > getmaxy()) {
        drop.y = 0;
        drop.x = rand() % getmaxx();
    }
}

int main() {
    int gd = DETECT, gm;
    initgraph(&gd, &gm, (char*)""); // Empty path is fine in WinBGIm

    srand(time(0));
    Raindrop raindrops[MAX_RAINDROPS];
    initializeRaindrops(raindrops, MAX_RAINDROPS);

    while (!kbhit()) {
        if (kbhit()) break;
        cleardevice();
        for (int i = 0; i < MAX_RAINDROPS; i++) {
            drawRaindrop(raindrops[i]);
            updateRaindrop(raindrops[i]);
        }
        delay(30);
    }

    closegraph();
    return 0;
}
