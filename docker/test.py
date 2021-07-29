import math
class Solution:
    def findMedianSortedArrays(self, nums1, nums2) -> float:
        nums1.extend(nums2)
        result = sorted(nums1)
        medium = (len(result))/2
        if medium % 1 == 0.5:
            print(int(medium))
            return result[int(medium)]
        else:
            print(2)
            return (result[int(medium-1)] + result[int(medium)])/2


if __name__=="__main__":
    ans = Solution().findMedianSortedArrays([1,2,3],[3,4])
    print(ans)