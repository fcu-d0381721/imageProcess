import pandas as pd

original = pd.read_csv('./test_result/original/submission.csv', encoding='utf-8')
two = pd.read_csv('./test_result/two/submission.csv', encoding='utf-8')
three = pd.read_csv('./test_result/three/submission.csv', encoding='utf-8')

print(three)
original = original[['image_filename','label_id','x','y','w','h','confidence']]
two = two[['image_filename','label_id','x','y','w','h','confidence']]
three = three[['image_filename','label_id','x','y','w','h','confidence']]
original = original.drop_duplicates(subset=['image_filename', 'label_id', 'x', 'y', 'w', 'h', 'confidence'], keep='first')
two = two.drop_duplicates(subset=['image_filename', 'label_id', 'x', 'y', 'w', 'h', 'confidence'], keep='first')
three = three.drop_duplicates(subset=['image_filename', 'label_id', 'x', 'y', 'w', 'h', 'confidence'], keep='first')
original = original.reset_index(drop=True)
two = two.reset_index(drop=True)
three = three.reset_index(drop=True)

original.to_csv('original.csv')
two.to_csv('two.csv')
three.to_csv('three.csv')