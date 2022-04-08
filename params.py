seed = 100

DEBUG = False 
dump_dataset = True
dataset = 'E1'
PE = False
query_path = None
#query_path = 'GPS-202108130219-randnum5'
#query_path = 'random'
#query_path = 'GPS-202109281627'
#query_path = 'baseline2'
load_from_checkpoint = None
#load_from_checkpoint = 'trained_models/E1/GPS-202109161735/model-latest' 
#dump_dataset = '202109161734'

class vae():
    latent_dim = 32
    beta_anneal_epoch = None 


class transformer():
    use = True
    self_att_only = False 
    vae = False 

    enc_layers = 4
    enc_hidden = 512
    enc_heads = 8
    enc_pf_dim = 1024

    dec_layers = enc_layers
    dec_hidden = enc_hidden 
    dec_heads = enc_heads
    dec_pf_dim = enc_pf_dim

    dropout = 0.1

    # useful when vae == True
    encode_method = 'first'
    past_emb = True 


################# Query #####################
diff_embedding = True
hard_softmax = True 

lr_scheduler_step_size = 100
gamma = 0.1
learn_rate = 0.0001
######### MI3 ########
dist_dim = 128 # == dense_output_size/2
ns_gamma = 1
distribution = 'Normal'
#distribution = 'Beta'
#distribution = 'GMM'

#### GMM ####
clusters = 4


######### MI2 ########
gumbel_softmax = False 
hellinger = False 
latent_code = True 

######### MI #########
t_space = True
io_recon = True
program_recon = True

lambda_ps  = 1.0
lambda_z_n = 0.001 
lambda_t_n = 0.0001 
lambda_z_t = 0.001 

lambda_io = 0.001
lambda_program = 0.001 
#############################################


# General training
num_epochs = 1000
patience = 20
#model_output_path = 'trained_models/E1/PE_model' #'trained_models/E1/GPS_model/'
if PE:
    model_output_path = 'trained_models/' + dataset + '/PE-'
else:
    model_output_path = 'trained_models/' + dataset + '/GPS-'


max_len = None #For debugging set a lower number, use None for running training for full data
if dataset == 'E1':
    max_prog_len = 4
else:
    max_prog_len = 12

# File params (Inference)
global_model_path = 'trained_models/'+dataset+'/GPS_model/best_model.th' #GPS model path
PE_model_path = 'trained_models/'+dataset+'/PE_model/best_model.th' #PE model path
result_path = 'results/'

# GPS and PE model training params
if PE:
    train_path = 'data/data/'+dataset+'/train_dataset_pe'
    val_path = 'data/data/'+dataset+'/val_dataset_pe'
else:
    train_path = 'data/data/'+dataset+'/train_dataset_gps'
    val_path = 'data/data/'+dataset+'/val_dataset_gps'
batch_size = int(32*2 / 4) 
val_iterator_size = 32

#    train_path = val_path

#Aggregator training params
att_batch_size = 100 #256

#Inference params
search_method = 'beam'
num_workers = 1
max_beam_size = 819200
dfs_max_width = 50
cab_beam_size = 100
cab_width = 10
cab_width_growth = 10

# DSL params
integer_min = -256
integer_max = 255
integer_range = integer_max - integer_min + 1
max_list_len = 20
num_inputs = 3
num_statements = 1298
num_operators = 38

# Program State Params
max_program_len = 8
max_program_vars = max_program_len + num_inputs
state_len = max_program_vars + 1
state_dim = 256

# H_theta and W_phi network params
type_vector_len = 2
embedding_size = 20
var_encoder_size = 56
dense_output_size = int(dist_dim * 2)
if distribution == 'GMM':
    dense_output_size = int((dist_dim * 2 + 1) * clusters)
dense_num_layers = 10
dense_growth_size = 56


############ query ps #############
if query_path is not None:
    print('Training with Queried Data!')
    train_path = 'trained_models/' + dataset + '/' + query_path + '/train_gps'
    val_path = 'trained_models/' + dataset + '/' + query_path + '/val_gps'
    if dataset == 'E2' and PE:
        batch_size = 256 
    elif (dataset == 'E1' and PE) or (dataset == 'E2' and not PE):
        batch_size = int(100 / 4)
    elif dataset == 'E1' and not PE:
        batch_size = int(32 / 4)
    dense_output_size = 256
    learn_rate = 0.001
    lr_scheduler_step_size = 8
    gamma = 0.1
###################################
############## debug ###############
if DEBUG:
    model_output_path = 'trained_models/debug/'
####################################
