//Library initialization
#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <mpi.h>
#include <time.h>
#include <cblas.h>

// Define the sparsity of the matrix M
#define SPARSITY 0.6

// Create a random sparse matrix by column
void randomMatriceM(int a, int b, double *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);
  
  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
      // Check if a random value between 0 and 1 is less than the sparsity factor
      if ((double)rand() / RAND_MAX < SPARSITY) {
        
        // Take a random number between 0 to 9
        A[a*j + i] = rand() % 10;  
      }
    }
  }
}

// Create a random matrix by row
void randomMatricev(int a, int b, double *A){

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

//Rearrange M by line 
void rearrange(int a,int b, double *A) {
  
  double *AR = (double *)calloc(a * b, sizeof(double));
  
  for (int i =0; i<a; i++) {
    for (int j=0; j<b; j++) {
    
      AR[b*i + j] = A[a*j + i];
    }
  
  }
  
  for (int i =0; i<a*b; i++) {
    A[i] = AR[i];
  } 
  
  free(AR);

}

// Function to determine the number of row to send each process and the resulting parameters
void determine_rownumbers(int m,int n,int k, int npes, int *Nnumbers,int *sendcountsM, int *displsM,int *sendcountsK, int *displsK) { 

  // if m is not a multiplier of process numbers
  if ((n%npes) != 0) {
  
    // Define the number of row for each process
    for (int i=0; i<npes; i++) {
    
      // Process balancing 
      if (i< (n%npes)) {
      
        Nnumbers[i] = ((n - (n%npes))/npes) + 1;  
    
    } else {
      Nnumbers[i] = ((n - (n%npes))/npes) ;
    }
  }
  
  } else {
  
    for (int i=0; i<npes; i++) {
    
      Nnumbers[i] = (n/npes);
    
    }
  
  }
  
  // Define the size of the rows to be sent to each process 
  for(int u=0; u<npes; u++) {
  
    sendcountsM[u] = Nnumbers[u] * m;
  }
  
  // Define the location in the matrix of items to be sent to each process 
  for(int j=1; j<npes; j++) {
  
    displsM[j] = displsM[j-1] + Nnumbers[j-1]*m;
  }
  
  
  // Define the size of the rows to be received by 0 for each process
  for(int u=0; u<npes; u++) {
  
    sendcountsK[u] = Nnumbers[u] * k ;
  }
  
  // Define the location in the matrix of items to be received by 0 for each process
  for(int j=1; j<npes; j++) {
  
    displsK[j] = displsK[j-1] + Nnumbers[j-1]*k;
  }

}


// Main function of algorithm 1 
int main(int argc, char *argv[]) {
  
  // MPI initialization
  int myrank, npes;
  MPI_Status status; 
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &npes);
  MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
  
  // Initialization of matrices parameters
  int m = atoi(argv[1]); 
  int n = atoi(argv[2]);
  int k = atoi(argv[3]);
  
  double *M = (double *)calloc(m * n, sizeof(double));
  double *v = (double *)calloc(n * k, sizeof(double)); 
  double *Mat = (double *)calloc(m * k, sizeof(double));
  
  // Initialization of communications parameters
  int *Nnumbers = (int *)calloc(npes, sizeof(int));
  int *sendcountsM = (int *)calloc(npes, sizeof(int));
  int *displsM = (int *)calloc(npes, sizeof(int));
  int *sendcountsK = (int *)calloc(npes, sizeof(int));
  int *displsK = (int *)calloc(npes, sizeof(int));
  
  determine_rownumbers(m,n,k, npes, Nnumbers,sendcountsM, displsM, sendcountsK, displsK);
  
  int N = Nnumbers[myrank];
  
  // Initialization of matricies for communications
  double *Msmall= (double *)calloc(m * N, sizeof(double));
  double *vsmall= (double *)calloc(N * k, sizeof(double));
  double *smallMat = (double *)calloc(m * k, sizeof(double));
  
  if(myrank == 0) {
   
    printf("\nAlgorithm3_cblas m:%d n:%d k:%d\n\n",m,n,k);
    
    // Creation of random matricies
  	randomMatriceM(m,n,M);
  	randomMatricev(n,k,v);
    
	}
   
  // Send columns and rows to processes
	MPI_Scatterv(M,sendcountsM,displsM, MPI_DOUBLE, Msmall, m*N,MPI_DOUBLE, 0,MPI_COMM_WORLD);
  MPI_Scatterv(v,sendcountsK,displsK, MPI_DOUBLE, vsmall, N*k,MPI_DOUBLE, 0,MPI_COMM_WORLD);
  
  if (myrank == 0) {
    printf("Msmall:\n");
    for (int i = 0; i < m*N; ++i) {
        printf("%f\t", Msmall[i]);
      }
    printf("\n\n");
    }
  
  rearrange(m,N,Msmall);
  
  if (myrank == 0) {
    printf("Msmall:\n");
    for (int i = 0; i < m*N; ++i) {
        printf("%f\t", Msmall[i]);
      }
      printf("\n\n");
    }
  
  // Matricies multiplication calculation
  cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, m, k, N, 1.0, Msmall, N, vsmall, k, 0.0, smallMat, k);
  
  // Group and sum the matricies to obtain a final matrix
  MPI_Reduce(smallMat, Mat, m*k, MPI_DOUBLE, MPI_SUM, 0,MPI_COMM_WORLD);
  
 
  if (myrank == 0) {
    printf("Mat:\n");
    for (int i = 0; i < m; ++i) {
      for (int j = 0; j < k; ++j) {
        printf("%f\t", Mat[j + k * i]);
      }
      printf("\n");
    }
    
    printf("\n\n\n");
    
  }
 
  MPI_Finalize();
  
  // Free the memory
  free(M);
  free(v);
  free(Mat);
  free(Msmall);
  free(vsmall);
  free(smallMat);
  
  return 0;
  
}
  
  
  
  
  
  