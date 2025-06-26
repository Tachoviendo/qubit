import os
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

# Ruta base donde estás trabajando
output_path = "/home/tacho/Documents/qubit/tts/qubitVoice_easy_train"

# Configuración del dataset
dataset_config = BaseDatasetConfig(
    formatter="ljspeech",
    meta_file_train="metadata.csv",
    path="/home/tacho/Documents/qubit/tts/voiceTrain"
)

# Configuración del modelo VITS
config = VitsConfig(
    batch_size=4,
    eval_batch_size=4,
    num_loader_workers=2,
    num_eval_loader_workers=2,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=200,
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="es-es",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    print_step=25,
    print_eval=True,
    mixed_precision=False,
    output_path=output_path,
    datasets=[dataset_config],
    use_language_embedding=False  # Si es multilingüe, activar
)

# Inicializar procesador de audio
ap = AudioProcessor.init_from_config(config)

# Inicializar tokenizer
tokenizer, config = TTSTokenizer.init_from_config(config)

# Cargar samples (text + audio)
train_samples, eval_samples = load_tts_samples(
    dataset_config,
    eval_split=True,
    eval_split_max_size=config.eval_split_max_size,
    eval_split_size=0.5,
)

# Inicializar modelo VITS
model = Vits(config, ap, tokenizer, speaker_manager=None)

# Inicializar trainer
trainer = Trainer(
    TrainerArgs(),
    config,
    output_path,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples
)

# ¡A entrenar!
trainer.fit()

