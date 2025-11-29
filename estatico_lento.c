#include <stdio.h>
#include <sys/time.h>

struct pix 
{
    unsigned int r, g, b;
};

// Se TAM não for passado pelo bash, roda com 1000 como segurança
#ifndef TAM
#define TAM 1000
#endif

// Alocação da matriz estática
struct pix color[TAM][TAM];

int main() 
{
    double ti, tf, tempo;
    struct timeval tempo_inicio, tempo_fim;

    // Warm-up: Inicializa a matriz para forçar alocação física da memória (Page Faults ocorrem aqui)
    int k, l;
    for (k = 0; k < TAM; k++) 
    {
        for (l = 0; l < TAM; l++) 
        {
            color[k][l].r = 1;
            color[k][l].g = 2;
            color[k][l].b = 3;
        }
    }

    gettimeofday(&tempo_inicio, NULL);

    int i, j;
    for (i = 0; i < TAM; i++) 
    {
        for (j = 0; j < TAM; j++) 
        {
            // Uso ineficiente da cache: acessa j -> i
            color[j][i].r = (color[j][i].r + color[j][i].g + color[j][i].b) / 3;
        }
    }

    gettimeofday(&tempo_fim, NULL);

    tf = (double)tempo_fim.tv_usec + ((double)tempo_fim.tv_sec * 1000000.0);
    ti = (double)tempo_inicio.tv_usec + ((double)tempo_inicio.tv_sec * 1000000.0);
    tempo = (tf - ti) / 1000.0;

    // Imprime apenas o tempo gasto para otimizar o CSV
    printf("%.3f", tempo);
    return 0;
}