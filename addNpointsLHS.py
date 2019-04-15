def addNpointsLHS(self,inMatrix, m=1, method='random'):
        """
        Add 'n' new points to the existing LHS matrix.
        NOTE:
            Assumes inMatrix to be a unit Hypercube i.e. all parameters are from 0-1
        :param m:
            How many new points do you want.
        :param method:
            'random' : choose a random value inside the bin
            'center' : choose the mid point of the bin
        :return:
        """
        # Validations.
        if not method in ['random', 'center']:
            print('Selected Method is invalid')
            return inMatrix
        if type(m) != int:
            print('"m" should be of type Integer')
            return inMatrix
        if m <= 0:
            print('"m" should be greater than 0')
            return inMatrix

        nRows = len(inMatrix[:, 0])
        nCols = len(inMatrix[0, :])

        # These are basically columnid/rowid taken at random.
        colVec = np.argsort(np.random.uniform(size=nCols))
        rowVec = np.argsort(np.random.uniform(size=nRows + m))

        # This new matrix will hold the new points.
        outMatrix = np.empty([nRows + m, nCols])
        outMatrix[:] = np.nan

        # Loop over each parameter at a time.
        for colId in colVec:
            newRow = -1

            # Loop over each bin.
            for rowId in rowVec:

                # Lower/Upper bound value of the new Bin
                lowerBound = float(rowId) / (nRows + m)
                upperBound = float(rowId + 1) / (nRows + m)

                # Compare all given point for the current paramater.
                # If there is no existing point in the new bin range then we add a new point.
                gtLowerBound = lowerBound <= inMatrix[:, colId]
                ltUpperBound = upperBound > inMatrix[:, colId]
                if not any(np.logical_and(gtLowerBound, ltUpperBound)):
                    newRow = newRow + 1

                    if method == 'random':
                        newPoint = np.random.uniform(low=lowerBound, high=upperBound, size=1)
                    else:
                        newPoint = lowerBound+ (upperBound-lowerBound)/2
                    outMatrix[newRow, colId] = newPoint

        # Drop All NANs
        outMatrix = outMatrix[~np.isnan(outMatrix).any(axis=1), :]
        
        if len(outMatrix)>=m:
            for i in range(len(outMatrix[0,:])):
                np.random.shuffle(outMatrix[:, i])
            
            outMatrix = np.concatenate((inMatrix, outMatrix[:m]), axis=0)
        else:
            print('Could not generate any new points')
            outMatrix = inMatrix

        # return
        return outMatrix