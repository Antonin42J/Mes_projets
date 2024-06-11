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

// Function to determine the number of row to send each process and the resulting parameters
void determine_rownumbers(int m,int n,int k, int npes, int *rownumbers,int *sendcountsN, int *displsN,int *sendcountsK, int *displsK) { 

  // if m is not a multiplier of process numbers
  if ((m%npes) != 0) {
  
    // Define the number of row for each process
    for (int i=0; i<npes; i++) {
    
      // Process balancing 
      if (i< (m%npes)) {
      
        rownumbers[i] = ((m - (m%npes))/npes) + 1;  
    
    } else {
      rownumbers[i] = ((m - (m%npes))/npes) ;
    }
  }
  
  } else {
  
    for (int i=0; i<npes; i++) {
    
      rownumbers[i] = (m/npes);
    
    }
  
  }
  
  // Define the size of the rows to be sent to each process 
  for(int u=0; u<npes; u++) {
  
    sendcountsN[u] = rownumbers[u] * n;
  }
  
  // Define the location in the matrix of items to be sent to each process 
  for(int j=1; j<npes; j++) {
  
    displsN[j] = displsN[j-1] + rownumbers[j-1]*n;
  }
  
  
  // Define the size of the rows to be received by 0 for each process
  for(int u=0; u<npes; u++) {
  
    sendcountsK[u] = rownumbers[u] * k ;
  }
  
  // Define the location in the matrix of items to be received by 0 for each process
  for(int j=1; j<npes; j++) {
  
    displsK[j] = displsK[j-1] + rownumbers[j-1]*k;
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
  
  //Timing variable : 
  double start_time_bcast, end_time_bcast, start_time_scatter, end_time_scatter, start_time_gather, end_time_gather, start_time_computation, end_time_computation;
  
  // Initialization of matrices parameters
  int m = atoi(argv[1]); 
  int n = atoi(argv[2]);
  int k = atoi(argv[3]);
  
  int *M = (int *)calloc(m * n, sizeof(int));
  int *v = (int *)calloc(n * k, sizeof(int)); 
  int *Mat = (int *)calloc(m * k, sizeof(int));
  
  // Initialization of communications parameters
  int *rownumbers = (int *)calloc(npes, sizeof(int));
  int *sendcountsN = (int *)calloc(npes, sizeof(int));
  int *displsN = (int *)calloc(npes, sizeof(int));
  int *sendcountsK = (int *)calloc(npes, sizeof(int));
  int *displsK = (int *)calloc(npes, sizeof(int));
  
  start_time_computation = MPI_Wtime();
  
  determine_rownumbers(m,n,k, npes, rownumbers,sendcountsN, displsN, sendcountsK, displsK);
  
  int r = rownumbers[myrank];
  
  // Initialization of matricies for communications
  int *Msmall= (int *)calloc(r * n, sizeof(int));
  int *smallMat = (int *)calloc(r * k, sizeof(int));
  
  if(myrank == 0) {
   
    printf("\nAlgorithm1 m:%d n:%d k:%d\n\n",m,n,k);
    
    // Creation of random matricies
  	randomMatriceM(m,n,M);
  	randomMatricev(n,k,v);
	}
 
  start_time_bcast = MPI_Wtime();
  
  // Broadcast matrix v to all process
  MPI_Bcast(v, n*k, MPI_INT, 0, MPI_COMM_WORLD);
  
  end_time_bcast = MPI_Wtime();
  
  start_time_scatter = MPI_Wtime();
  
  // Send rows to processes
	MPI_Scatterv(M,sendcountsN,displsN, MPI_INT, Msmall, r*n,MPI_INT, 0,MPI_COMM_WORLD);
 
  end_time_scatter = MPI_Wtime();
  
  // Matricies multiplication calculation
  MatrixMultiplication( r, n, k, Msmall, v, smallMat);
  
  start_time_gather = MPI_Wtime();
  
  // Group the final rows in a matrix
	MPI_Gatherv(smallMat, r*k,MPI_INT, Mat, sendcountsK, displsK,MPI_INT,0,MPI_COMM_WORLD);
 
  end_time_gather = MPI_Wtime();
  
  end_time_computation = MPI_Wtime();
 
  if (myrank == 0) {
  
    printf("Cost of Bcast : %fs \n", end_time_bcast - start_time_bcast);
    printf("Cost of Scatter : %fs\n", end_time_scatter - start_time_scatter);
    printf("Cost of Gather : %fs\n", end_time_gather - start_time_gather);
    printf("Cost of communication : %fs \n\n", (end_time_bcast - start_time_bcast) + (end_time_scatter - start_time_scatter) + (end_time_gather - start_time_gather)); 
    
    printf("Cost of computation : %fs \n", (end_time_computation - start_time_computation) - ((end_time_bcast - start_time_bcast) + (end_time_scatter - start_time_scatter) + (end_time_gather - start_time_gather)));
    printf("Total time : %fs\n",end_time_computation - start_time_computation );
  }
 
  MPI_Finalize();
  
  // Free the memory
  free(M);
  free(v);
  free(Mat);
  free(Msmall);
  free(smallMat);
  
  return 0;
  
}
  
  
  
  
  
  