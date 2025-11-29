#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

struct pix 
{
    unsigned int r, g, b;
};

// Se TAM não for passado pelo bash, roda com 1000 como segurança
#ifndef TAM
#define TAM 1000
#endif

int main() 
{
    struct pix *color = malloc((size_t)TAM * TAM * sizeof(struct pix));
    if (!color) 
    { 
        printf("ERRO malloc\n"); 
        return 1; 
    }

    for (size_t i = 0; i < (size_t)TAM * TAM; i++)
        color[i] = (struct pix){1,2,3};

    double ti, tf, tempo;
    struct timeval tempo_inicio, tempo_fim;

    gettimeofday(&tempo_inicio, NULL);

    size_t i, j;
    for (i = 0; i < TAM; i++) 
    {
        for (j = 0; j < TAM; j++) 
        {
            color[j * (size_t)TAM + i].r = (color[j * (size_t)TAM + i].r + color[j * (size_t)TAM + i].g + color[j * (size_t)TAM + i].b) / 3;
        }
    }

    gettimeofday(&tempo_fim, NULL);

    tf = (double)tempo_fim.tv_usec + ((double)tempo_fim.tv_sec * 1000000.0);
    ti = (double)tempo_inicio.tv_usec + ((double)tempo_inicio.tv_sec * 1000000.0);
    tempo = (tf - ti) / 1000.0;

    // Imprime apenas o tempo gasto para otimizar o CSV
    printf("%.3f", tempo);
    free(color);
    return 0;
}