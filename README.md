# Projekt 2DBP - README

## Opis projektu

Projekt realizuje algorytmy rozwiązywania problemu dwuwymiarowego pakowania w strip (2D Strip Packing Problem) z wykorzystaniem heurystyk (Bottom-Left, Bottom-Left-Fill) oraz metaheurystyk (Simulated Annealing, Genetic Algorithm).

---

## Struktura katalogów

- `Projekt_2DBP/`
  - `model/` — definicje instancji, przedmiotów, rozmieszczeń, rozwiązań
  - `heuristics/` — heurystyki dekodujące permutacje
  - `metaheuristics/` — metaheurystyki optymalizujące permutacje
  - `data/` — loader instancji, przykładowe dane

---

## Najważniejsze klasy

### model/instance.py

**BinPackingInstance**

- Pola:
  - `width` — szerokość stripu
  - `items` — lista obiektów do zapakowania
- Funkcje:
  - `from_file(path)` — ładuje instancję z pliku

### model/item.py

**Item**

- Pola:
  - `id` — identyfikator
  - `width`, `height` — rozmiary obiektu

### model/placement.py

**Placement**

- Pola:
  - `item` — obiekt typu `Item`
  - `id` — identyfikator obiektu
  - `x`, `y` — pozycja lewego dolnego rogu
  - `width`, `height` — rozmiary obiektu
  - `bin_id` — identyfikator pojemnika (domyślnie 0)
- Właściwości:
  - `area` — pole powierzchni obiektu
  - `right`, `top` — współrzędne prawej i górnej krawędzi
- Funkcje:
  - `intersects(other)` — sprawdza kolizję z innym rozmieszczeniem
  - `inside_strip(strip_width)` — sprawdza, czy rozmieszczenie mieści się w stripie
  - `__repr__()` — tekstowa reprezentacja rozmieszczenia

**PackingResult**

- Pola:
  - `placements` — lista rozmieszczeń

### model/solution.py

**Solution**

- Pola:
  - `permutation` — permutacja obiektów
  - `placements` — lista rozmieszczeń
  - `fitness` — wartość funkcji celu
- Funkcje:
  - `evaluate(instance, decoder, fitness_evaluator)` — dekoduje permutację i ocenia rozwiązanie
  - `is_evaluated()` — czy rozwiązanie zostało ocenione
  - `copy()` — kopia rozwiązania

---

### heuristics/decoder.py

**Decoder**

- Bazowa klasa dla heurystyk dekodujących permutacje na rozmieszczenia.
- Funkcja:
  - `decode(instance, permutation)` — zwraca listę rozmieszczeń

### heuristics/bottomleft.py

**BottomLeft**

- Dziedziczy po `Decoder`.
- Implementuje klasyczną heurystykę Bottom-Left.
- Funkcja:
  - `decode(instance, permutation)` — rozmieszcza obiekty wg reguły BL

### heuristics/bottom_left_fill.py

**BottomLeftFill**

- Dziedziczy po `Decoder`.
- Implementuje heurystykę Bottom-Left-Fill (BLF).
- Funkcja:
  - `decode(instance, permutation)` — rozmieszcza obiekty wg reguły BLF

---

### metaheuristics/sa.py

**SimulatedAnnealing**

- Pola:
  - `current_solution` — aktualne rozwiązanie
  - `best_solution` — najlepsze znalezione rozwiązanie
  - `T`, `T_min`, `alpha`, `max_iter` — parametry algorytmu
- Funkcje:
  - `neighbor(solution)` — generuje sąsiada przez inwersję permutacji
  - `accept(delta)` — reguła akceptacji
  - `run(instance)` — uruchamia algorytm SA

### metaheuristics/ga/ga.py

**GeneticAlgorithm**

- Pola:
  - `population` — lista rozwiązań
  - `decoder`, `fitness_evaluator` — obiekty do oceny
  - `mutation_rate`, `crossover_rate`, `generations` — parametry GA
- Funkcje:
  - `select()` — selekcja turniejowa
  - `crossover(parent1, parent2)` — krzyżowanie
  - `mutate(solution)` — mutacja
  - `run(instance)` — uruchamia algorytm GA

---

## Loader danych

### data/loader.py

**Loader**

- Funkcje:
  - `load_instance(path)` — ładuje instancję z pliku

---

## Fitness

### fitness.py

**FitnessEvaluator**

- Klasa bazowa do oceny rozwiązań (abstrakcyjna).
- Funkcja:
  - `evaluate(placements)` — oblicza wartość funkcji celu na podstawie rozmieszczeń

**HeightFitnessEvaluator**

- Dziedziczy po `FitnessEvaluator`.
- Funkcja:
  - `evaluate(placements)` — zwraca maksymalną wysokość rozmieszczeń (im niższa, tym lepiej)

---

---

### constructive_permutation/permutation_generator.py

**PermutationGenerator**

- Klasa bazowa dla heurystyk generujących permutacje.
- Funkcja:
  - `generate(instance)` — zwraca permutację identyfikatorów obiektów

**GreedyAreaPermutationGenerator**

- Dziedziczy po `PermutationGenerator`.
- Funkcja:
  - `generate(instance)` — sortuje obiekty malejąco wg pola powierzchni (width \* height)

**RandomGenerator**

- Dziedziczy po `PermutationGenerator`.
- Funkcja:
  - `generate(instance)` — zwraca losową permutację obiektów

---

### visualizer.py

**Visualizer**

- Klasa do wizualizacji rozmieszczeń rozwiązania 2D Strip Packing.
- Funkcja statyczna:
  - `draw_solution(placements, bin_width, filename, best_fitness)` — rysuje rozmieszczenie i zapisuje do pliku lub wyświetla
