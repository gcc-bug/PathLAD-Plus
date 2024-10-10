#include <stdbool.h>
#include "global.h"

int main(){
    int nbIsolatedP;
    Tgraph *Gp = createGraph("test_graph.txt",true,&nbIsolatedP);
    printf("try print\n");
    // // printGraph(Gp);
    int i, j, k;
    if (Gp->isDirected)
        printf("Directed ");
    else
        printf("Non directed ");
    // printf("graph with %d vertices\n",Gp->nbVertices);
    // for (i=0; i<Gp->nbVertices; i++){
    //     printf("Vertex %d has %d adjacent vertices: ",
    //            i,Gp->nbAdj[i]);
    //     for (j=0; j<Gp->nbAdj[i]; j++){
    //         k = Gp->adj[i][j];
    //         if (Gp->edgeDirection[i][k] == 1)
    //             printf(" %d(succ)",k);
    //         else if (Gp->edgeDirection[i][k] == 2)
    //             printf(" %d(pred)",k);
    //         else if (Gp->edgeDirection[i][k] == 3)
    //             printf(" %d(succ and pred)",k);
    //         else
    //             printf("error !");
            
    //     }
    //     printf("\n");
        
    // }
    return 0;
}