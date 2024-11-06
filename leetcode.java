class Solution {
  public void merge(int[] nums1, int m, int[] nums2, int n) {
    int[] tmp = new int[m];
    System.arraycopy(nums1, 0, tmp, 0, m);
    
    int oneidx = 0;
    int twoidx = 0;
    int i = 0;
    
    while (oneidx < m && twoidx < n) {
      if (tmp[oneidx] <= nums2[twoidx]) {
        nums1[i] = tmp[oneidx];
        oneidx++;
      } else {
        nums1[i] = nums2[twoidx];
        twoidx++;
      }
      i++;
    }
    
    while (oneidx < m) {
      nums1[i] = tmp[oneidx];
      oneidx++;
      i++;
    }
    
    while (twoidx < n) {
      nums1[i] = nums2[twoidx];
      twoidx++;
      i++;
    }
  }
}