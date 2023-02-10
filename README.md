1) If these commands don't work in Windows, create folders manually.<br>
```mkdir data```<br>
```mkdir static/audio```<br>
2) Create a conda environment with Python 3.6 preferably (open ananconda bash in this directory if windows)<br>

```conda create -n allennlp -c conda-forge allennlp python=3.6```<br>

3) Activate the environment<br>
```conda activate allennlp```<br>
<br>
4) Install other requirements<br>

```pip install -r requirements.txt```<br>
```python app.py```
