from mmaction.apis import inference_recognizer, init_recognizer

label_to_class_name = {
    0: 'S80',
    1: 'S120',
    2: 'S150',
    3: 'S180'
}

#####################    Only modigy this part    ##########################

# Our Deep learning model
config_path = 'C:\\Users\\Administrator\\kichang\\mmaction2_for_deploy\\model.py'
# Training record
checkpoint_path = 'C:\\Users\\Administrator\\Documents\\GitHub\\work_dirs\\model\\20231215_212155_0.835_ending_16_frame\\best_acc_top1_epoch_265.pth'
# Video file
img_path = 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_ending16\\221007Cheonan-new400data\\S120\\18-120_1.avi_labeled.avi_48frame_extracted.avi'

############################################################################

# build the model from a config file and a checkpoint file
model = init_recognizer(config_path, checkpoint_path, device="cpu")  # device can be 'cuda:0'

# test a single image
result = inference_recognizer(model, img_path)

# Extract the predicted label tensor and convert it to an integer
pred_label_tensor = result.pred_label
pred_label = pred_label_tensor.item()  # Convert tensor to integer

# Get the class name using the predicted label
class_name = label_to_class_name.get(pred_label, "Unknown")

# Print the class name as the result
print(f"Predicted Class for the video: {class_name}")