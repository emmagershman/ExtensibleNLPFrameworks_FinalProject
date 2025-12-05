from letters import Letters
import pprint as pp

def main():
    letters = Letters()
    letters.load_text('data/DearLittleGirl_02-01-1915.txt', label='Dear Little Girl, February 1915')
    letters.load_text('data/DearLittleSweetheart_05-31-1915.txt', label='Dear Little Sweetheart, May 1915')
    letters.load_text('data/DearLittleGirl_06-09-1915.txt', label='Dear Little Girl, June 1915')
    letters.load_text('data/DearestSweetestLittleGirlie_06-15-1915.txt', label='Dearest Sweetest Little Girlie, June 1915')
    letters.load_text('data/DearDarlingNell_04-28-1917.txt', label='Dear Darling Nell, April 1917')
    letters.load_text('data/DearDaddy_09-1916.txt', label='Dear Daddy, September 1916')
    letters.load_text('data/MyDearestWill_03-28-1917.txt', label='My Dearest Will, March 1917')
    letters.load_text('data/DearGertie_05-06-1916.txt', label='Dear Gertie, May 1916')
    pp.pprint(letters.data)
    letters.compare_num_words()
    #letters.second_visualization()
    letters.word_cloud()
    letters.third_visualization()

if __name__ == '__main__':
    main()