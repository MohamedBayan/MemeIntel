# ArMeme Dataset

## Overview

ArMeme is the first multimodal Arabic memes dataset that includes both text and images, collected from various social media platforms. It serves as the first resource dedicated to Arabic multimodal research. While the dataset has been annotated to identify propaganda in memes, it is versatile and can be utilized for a wide range of other research purposes, including sentiment analysis, hate speech detection, cultural studies, meme generation, and cross-lingual transfer learning. The dataset opens new avenues for exploring the intersection of language, culture, and visual communication.

## Sample Metadata

| Field         | Description |
|---------------|-------------|
| **ID**        | `data/arabic_memes_fb_insta_pinterest/Instagram/IMAGES/8yerjaw/2022-01-27_13-44-00_UTC.jpg` |
| **Text**      | `- لما تدعي على اخوك، وبعدين تندم = يارب ما يموت` |
| **Image Path**| `./data/arabic_memes_fb_insta_pinterest/Instagram/IMAGES/8yerjaw/2022-01-27_13-44-00_UTC.jpg` |
| **Class Label**| `propaganda` |
| **Explanation (EN)** | The image features a cartoon character, Tom from *Tom and Jerry*, lying in bed with a worried expression, accompanied by Arabic text. The text translates to: “Why do you curse your brother and then regret it = Oh God, don’t let him die.” This meme combines humor with a dark undertone, trivializing the act of cursing someone and then fearing the consequences. The human expert likely classified it as propaganda due to the normalization of harmful language and its emotional manipulation through humor, especially in contexts where familial respect is culturally significant. |
| **Explanation (AR)** | الصورة تستخدم شخصية كرتونية معروفة (توم من توم وجيري) في وضعية تعبيرية مضحكة ومبالغ فيها، مع نص باللهجة العامية العربية. النص يتحدث عن الشعور بالندم بعد الدعاء على الأخ، مما يثير مشاعر الذنب والقلق بشكل ساخر. هذا المزج بين الصورة والنص يهدف إلى التأثير العاطفي باستخدام الفكاهة والسخرية، وهو أسلوب شائع في الدعاية لإيصال رسالة أو تعزيز فكرة معينة. التلاعب بالمشاعر من خلال المزاح والسياق الثقافي يجعل الصورة تصنف كدعاية. |

---

## ArMeme Dataset Description

For full access to the dataset, see the [official ArMeme page on Hugging Face](https://huggingface.co/datasets/QCRI/ArMeme).

- **Language:** Arabic  
- **Modality:** Multimodal (text + image)  
- **Total Samples in Full Dataset:** ~6000  
- **Splits:** `train`, `dev`, `test`

Each data point in the full dataset includes:
- `id`: Unique identifier
- `text`: Meme caption or extracted OCR text
- `img_path`: Local path to the image
- `class_label`: e.g., propaganda, non-propaganda
- `explanation_en` / `explanation_ar`: Expert-provided justifications *(available in some versions)*

---

## License

This dataset is licensed under the **CC-By-NC-SA-4.0** license.

## Citation

```
@misc{kmainasi2025memeintelexplainabledetectionpropagandistic,
      title={MemeIntel: Explainable Detection of Propagandistic and Hateful Memes}, 
      author={Mohamed Bayan Kmainasi and Abul Hasnat and Md Arid Hasan and Ali Ezzat Shahroor and Firoj Alam},
      year={2025},
      eprint={2502.16612},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.16612}, 
}
```


```
@article{alam2024armeme,
  title={{ArMeme}: Propagandistic Content in Arabic Memes},
  author={Alam, Firoj and Hasnat, Abul and Ahmed, Fatema and Hasan, Md Arid and Hasanain, Maram},
  year={2024},
  journal={arXiv: 2406.03916},
}
```

