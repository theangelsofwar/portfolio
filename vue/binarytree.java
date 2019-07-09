// you can also use imports, for example:
// import java.util.*;
import java.util.ArrayList;
// you can write to stdout for debugging purposes, e.g.
// System.out.println("this is a debug message");

class Solution {
    public int solution(Tree T) {
        // write your code in Java SE 8
        
        //binary search
        int data=T.x;
        Tree r=T.r; 
        Tree l=T.l; //left and right children trees
       ArrayList<Tree> leftnodes=new ArrayList<Tree>();
       ArrayList<Tree> rightnodes=new ArrayList<Tree>(); //track nodes data
        
        leftnodes.add(l);
        rightnodes.add(r);
        int nodescounter=0; //at the root, the distinct nodescounter/pathcounter
        
        //anything recurse can do iteratively
        
        int rightcount=0;
        
       int leftcount=0;
        
        while(r!=null)
        {
            
            Tree current=r;
            if(current.x!=data)
            {
                rightcount++;
                rightnodes.add(current);
            }
            
            return 1+solution(T.r);
        }
        
        
        while(l!=null)
        {
            
            Tree current=l;
            if(current.x!=data){
                leftcount++;
                leftnodes.add(current);
            }
            
            
            return 1+solution(T.l);
        }
        
        
        
        if(rightcount>leftcount)
        {
           nodescounter=rightcount;    
        }
        else{
            nodescounter=leftcount;
        }
        
        
        return nodescounter;
        
    }
}[]