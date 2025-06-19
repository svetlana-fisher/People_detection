### Инструкция по запуску и использованию модели
Скачайте test.zip в нём находится всё что нужно для использования готовой модели  
Затем рекомендуется создать виртуальное окружение  
для Linux
>python3 -m venv venv  
>source venv/bin/activate

для Windows  
>python3 -m venv venv  
>.venv/Scripts/activate

в него необходимо установить нужные зависимости  
>pip install -r requirements.txt

Затем запустите программу start.py у неё есть передаваемые агрументы -i "file_path входная картинка" -o "file_path выходная картинка" --conf "Confidence threshold"  
пример  
>python start.py -i input.jpg -o output.jpg

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

