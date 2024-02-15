from pickletools import optimize
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir = '/Users/leviharris/Desktop/shot-quality-estimation/ex_img_only/finetune_vgg/dataset/train'
validation_dir = '/Users/leviharris/Desktop/shot-quality-estimation/ex_img_only/finetune_vgg/dataset/val'

# some augmentations
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# TODO: try a sigmoid
val_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=128,
    class_mode='binary' # since we use binary_crossentropy
)

# TODO: try a sigmoid
validation_generator = val_datagen.flow_from_directory(
    validation_dir,
    target_size=(224, 224),
    batch_size=128,
    class_mode='binary'
)

base = ResNet50(
    weights = 'imagenet',
    include_top = False
)

# freeze all layers in the neck of the model
for layer in base.layers:
    layer.trainable = False 

x = base.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
pred = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base.input, outputs=pred)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator, epochs=100, validation_data=validation_generator, verbose=1)

# for layer in base.layers[:165]:
#     layer.trainable = False
# for layer in base.layers[165:]:
#     layer.trainable = True

# # Recompile the model for fine-tuning
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# # Fine-tune the model
# model.fit(train_data, train_labels, epochs=10, validation_data=(validation_data, validation_labels))
