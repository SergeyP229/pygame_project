# Galaxy shooter

## 1. Задачи проекта

Написать игру Galaxy shooter на Python, используя библиотеку Pygame

Приложение должно иметь следующие функции:

* игрок должен уметь передвигаться и стрелять
* у игрока должен быть выбор одного из двух режимов (бесконечный и уровни)
* Подсчитывать очки игрока и показывать их в конце игры


## 2. Установка и запуск приложения

Приложение протестировано для Python версии 3.9.
Для установки зависимостей приложения создайте новое виртуальное окружение Python 3, активируйте его и выполните команду

```
pip install -r requirements.txt
```

После этого приложение можно будет запустить командой
```
python3 main.py
```
Или, при работе с *nix, командой
```
./main.py
```

## 3. Работа с приложением

Работа с приложением производится через окно Pygame.

### 3.1 Главное меню
Здесь находятся три кнопки. Первая - PLAY, она запускает бесконечный режим.
Игра будет продолжаться до тех пор, пока у игрока не закончится здоровье.
Если здоровье закончится, откроется финальное окно. 
Игрок может передвигаться, но не выходя за рамки окна, и стрелять. Супервыстрел отличается от обычного только тем, что не уничтожается после первого столкновения, а пролетает все поле.
Каждое попадание по вражескому кораблю заряжает супер выстрел(для полной зарядки требуется 5 попаданий) и начисляет очки,
в зависимости от уровня вражеского корабля.

За определенные промежутки времени в случайных местах поля будут появляться враги,
которые будут стрелять по игроку. При столкновении игрока с врагом враг будет уничтожаться, а игрок получать урон.
При попадании вражеского выстрела игрок также теряет здоровье. Вражеский корабль уничтожается, когда:
* выстрел игрока сталкивается с врагом
* игрок сталкивается с врагом
* враг сталкивается с другим врагом
* враг сталкивается с метеоритом
Каждый вражеский корабль имеет свой уровень (1-5), от которого зависят его характеристики (скорость, урон),
изображение и изображение выстрела.
Вражеские корабли постоянно двигаются и иногда меняют направление движения.

Помимо вражеских кораблей на поле появляются метеориты. Они двигаются, но не меняют направление движения и скорость.
Сами скорость и направление движения задаются при создании метеорита случайным образом в определенном диапазоне,
также из нескольких возможных выбирается случайное изображение.
Метеорит уничтожается, если сталкивается с игроком, выстрелом игрока, другим метеоритом или вражеским кораблем.
При столкновении игрока и метеорита игрок также получает урон.

Также, каждые 20 секунд появляется один из пяти возможных бонусов: тройной выстрел (вместо одного снаряда игрок выпускает три),
супервыстрел (заряжает супервыстрел), бафф на скорость (скорость игрока увеличивается в два раза),
щит (любой следующий урон по игроку аннулируется), восстановление здоровья (игрок получает +50 здоровья, даже если у него полный запас здоровья)
Бонусы тройного выстрела и баффа на скорость действуют только 20 секунд, пока не появится новый бонус.

Вторая кнопка - LEVELS, при ее нажатии создастся окно выбора уровня.

Третья кнопка - EXIT, она закрывает игру.


### 3.2 Окно выбора уровня
Здесь игрок может выбрать один из трех уровней.
При запуске любого уровня игрок появляется в определенном месте. Цель - достичь противоположного по диагонали угла поля,
где находится вращающийся портал. В Определенных местах будут находиться вражеские корабли, но двигаться они не будут, только стрелять, и
будут пролетать метеориты.
Если у игрока закончится здоровье, то также откроется финальное окно.
Если игрок достигнет цель, откроется победное окно.
В режиме "уровни" отсутствуют бонусы, но зато имеются перегородки, загораживающие игроку путь.

### 3.3 Финальное окно
Здесь игрок может выйти из игры или вернуться в главное меню. В окне показывается, сколько очков набрал игрок.

### 3.4 Победное окно
Здесь игрок может вернуться в главное меню или начать следующий уровень. В окне отображается количество звезд (1-3).
Количество звезд зависит от того, сколько здоровья осталось у игрока.


В течение всей игры проигрываются разные звуки: фоновая музыка, звук выстрела игрока, звук выстрела вражеского корабля, звук столкновения,
звук взрыва, победный и проигрышный звуки, звук сбора бонуса и звук супер выстрела.



В игру можно добавлять свои уровни, изменяя файлы уже существующих уровней.
Все строки должны начинаться с "CREATE".
"place_spawn x y" задает начальное положение игрока в точке (x;y);
"place_over x y" задает конечное положение игрока в точке (x;y);
"Obstacle x y" создает перегородку в точке (x;y);
"Enemy x y level" создает вражеский корабль в точке (x;y) с уровнем level (1-5);
"Meteor x y speed_x speed_y" создает метеорит в точке (x;y), с направлением speed_x speed_y (начало координат - левый верхний угол).

Решение о необходимости добавления функционала редактирования будет приниматься по итогам эксплуатации.