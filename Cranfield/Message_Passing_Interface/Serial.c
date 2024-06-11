//Library initialization
#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <mpi.h>
#include <time.h>

// Define the sparsity of the matrix M
#define SPARSITY 0.6

// Create a random sparse matrix by row
void randomMatriceM(int a, int b, int *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);
  
  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
      // Check if a random value between 0 and 1 is less than the sparsity factor
      if ((double)rand() / RAND_MAX < SPARSITY) {
        
        // Take a random number between 0 to 9
        A[b*i + j] = rand() % 10;  
      }
    }
  }
}

// Create a random matrix by row
void randomMatricev(int a, int b, int *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);

  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
    
      // Take a random number between 0 to 9 ...
      A[b*i + j] = rand() % 10; 
      
      // ... but change if it is 0
      if (A[b*i + j] == 0) {
   	    A[b*i + j] = rand() % 10 + 1;
      } 
    }
  }
}


// Multiplication of two matricies
void MatrixMultiplication(int m, int n, int k, int *M,int *v, int *Mat) {
 
  // Browse rows, columns and the shared dimension
  for(int i=0; i<m; i++) {
    for(int j=0; j<k; j++) {
      int newpoint=0;
      for(int u=0; u<n;u++) {
        newpoint += M[n * i + u] * v[j + u * k];
      }
    Mat[i*k + j] = newpoint; 
    }
  }
}

// Main function of algorithm 1 
int main(int argc, char *argv[]) {
  
  //Initalisation csv
  FILE *file;
  
  // MPI initialization
  int myrank,npes;
  MPI_Status status; 
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &npes);
  MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
  
  //Time initalization 
  double start, end;
  start = MPI_Wtime();
  
  // Initialization of matrices parameters
  int m = atoi(argv[1]); 
  int n = atoi(argv[2]);
  int k = atoi(argv[3]);
  
  int *M = (int *)calloc(m * n, sizeof(int));
  int *v = (int *)calloc(n * k, sizeof(int)); 
  int *Mat = (int *)calloc(m * k, sizeof(int));
  
  if(myrank == 0) {
   
    printf("\nSerial m:%d n:%d k:%d\n\n",m,n,k);
    
    // Creation of random matricies
  	randomMatriceM(m,n,M);
  	randomMatricev(n,k,v);
  
    // Matricies multiplication calculation
    MatrixMultiplication( m, n, k, M, v, Mat);
  
  
    end = MPI_Wtime();
  
    double total_time = end - start;
   
    printf("Total time : %fs\n", total_time ); 
    
    //Write data into csv  
    file = fopen("time.csv","a");
   
    fprintf(file,"\n%d,%d,%d,%s,%f,%d", m,n,k, "Serial", total_time, npes);
    
    fclose(file);
  }
 
  MPI_Finalize();
  
  // Free the memory
  free(M);
  free(v);
  free(Mat);
  
  return 0;
  
}
  
  
  
  
  
  