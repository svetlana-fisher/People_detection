## Инструкция по запуску и использованию модели
### Скачивание необходимого набора файлов  
1. Откройте командную строку
2. С помощью команды cd перейдите в папку в которую вы хотите сохранить файлы
3. введите следующие команды
>git clone git@github.com:svetlana-fisher/People_detection_zip.git  
>cd People_detection_zip

Затем рекомендуется создать виртуальное окружение  
для Linux
>python -m venv venv  
>source venv/bin/activate

для Windows  
>python -m venv venv  
>venv/Scripts/activate

в него необходимо установить нужные зависимости  
>pip install -r requirements.txt

Затем запустите программу start.py у неё есть передаваемые агрументы -i "input_folder_path" -o "output_folder_path" --conf "Confidence threshold"  
пример  
>python start.py -i input -o output

## Обучение
![results.png](results.png)

**P_curve** | **R_curve**
:-------------------------:|:-------------------------:
| ![P_curve.png](P_curve.png) | ![R_curve.png](R_curve.png) |

### PR_curve
![PR_curve.png](PR_curve.png)

### train_batch
![train_batch2.jpg](train_batch2.jpg) 

### val_batch
![val_batch0_pred.jpg](val_batch0_pred.jpg)

## Итоговая map0.5
> ### 0.8726

