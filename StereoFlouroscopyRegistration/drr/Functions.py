def ChangeImageDirection(oldDirection,newDirection,DimensionOut):
    '''
    ChangeImageDirection(oldDirection,newDirection,DimensionOut)
        Changes the old Direction to a new direction (given the image dimension).
        Input Arguments: 
            oldDirection : The original direction of the image e.g. image.GetDirection() 
            newDirection : The direction that we like to set the image direction to. 
            DimensionOut : The dimension of the image that we like to output (2D or 3D)
            
    '''
    #%%
    vnlMatrix = oldDirection.GetVnlMatrix()
    for i in range(DimensionOut):
        for j in range(DimensionOut):
            vnlMatrix.put(i,j,newDirection[i,j])


       #%% 
def PrintDirection(imageDirection,DimensionOut):
    vnlMatrix = imageDirection.GetVnlMatrix()
    for i in range(DimensionOut):
        for j in range(DimensionOut):
            print "{:>8.4f}".format(vnlMatrix.get(i,j)),
        print
        