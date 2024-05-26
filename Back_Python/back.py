from joblib import dump, load
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

model_knn_go0 = load('models/model_knn_0_mono.joblib')
le_go0 = load('models/label_encoder_go0.joblib')

model_knn_go1 = load('models/model_knn_1_mono.joblib')
le_go1 = load('models/label_encoder_go1.joblib')

namespaces = {
    'GO:0003674': 'molecular_function',
    'GO:0008150': 'biological_process',
    'GO:0005575': 'cellular_component'
}

max_seq_length = 1695
model_lstm_go0 =  load_model('models/model_lstm_0.h5')
le_lstm_go0 = load('models/label_encoder_lstm_0.joblib')
scaler = load("models/scaler.save")

def separate_into_codons(dna_seq):
    codons = [(dna_seq[i:i+3]) for i in range(0, len(dna_seq), 3)]
    return(codons)

def codon_to_protein(codon):
    prot = ''
    if len(codon)==3:
        if codon[0] == 'T':
            if codon[1] == 'T':
                if codon[2] == 'T' or codon[2] == 'C':
                    # phenylalanine
                    prot = 'F' # 'Phe'
                else:
                    # Leucine
                    prot = 'L' # 'Leu'
            elif codon[1] == 'C':
                # Serine
                prot = 'S' # "Ser"
            elif codon[1] == 'A':
                if codon[2] == 'T' or codon[2] == 'C':
                    # Tyrosine
                    prot = 'Y' # 'Tyr'
                else:
                    # Stop
                    # prot = 'Stop'            
                    prot = ''   
            elif codon[1] == 'G':
                if codon[2] == 'T' or codon[2] == 'C':
                    # Cysteine
                    prot = 'C' # 'Cys'
                elif codon[2] == 'A':
                    # Stop
                    #prot = 'Stop'
                    prot = ''   
                else:
                    # Tryptophan
                    prot = 'W' # 'Trp'

        if codon[0] == 'C':
            if codon[1] == 'T':
                # Leucine
                prot = 'L' # 'Leu'
            elif codon[1] == 'C':
                # Proline
                prot = 'P' # 'Pro'
            elif codon[1] == 'A':
                if codon[2] == 'T' or codon[2] == 'C':
                    # Histidine
                    prot = 'H' # 'His'
                else:
                    # Glutamine
                    prot = 'Q' # 'Gln'
            elif codon[1] == 'G':
                # Arginine
                prot = 'R' # 'Arg'

        if codon[0] == 'A':
            if codon[1] == 'T':
                if codon[2] == 'T' or codon[2] == 'C' or codon[2] == 'A':
                    # Isoleucine
                    prot = 'I' # 'Ile'
                else:
                    # Methionine
                    prot = 'M' # 'Met' 
            elif codon[1] == 'C':
                # Threonine
                prot = 'T' # 'Thr'
            elif codon[1] == 'A':
                if codon[2] == 'T' or codon[2] == 'C':
                    # Asparagine
                    prot = 'N' # 'Asn'
                else:
                    # Lysine
                    prot = 'K' # 'Lys'
            elif codon[1] == 'G':
                if codon[2] == 'T' or codon[2] == 'C':
                    # Serine
                    prot = 'S' # 'Ser'
                else:
                    # Arginine
                    prot = 'R' # 'Arg'

        if codon[0] == 'G':
            if codon[1] == 'T':
                # Valine
                prot = 'V' # 'Val'
            elif codon[1] == 'C':
                # Alanine
                prot = 'A' # 'Ala'
            elif codon[1] == 'A':
                if codon[2] == 'T' or codon[2] == 'C':
                    # Aspartic Acid
                    prot = 'D' # 'Asp'
                else:
                    # Glutamic Acid
                    prot = 'E' # 'Glu'
            elif codon[1] == 'G':
                # Glycine
                prot = 'G' # 'Gly'
    else:
        # prot = 'IDK'
        prot=''
    return prot

def compute_sequence_proteins(codons):
    proteins = []
    for cod in codons:
        protein = codon_to_protein(cod)
        proteins.append(protein)
        # print(cod, prot)
    return proteins

def compute_protein(dna_sequence):
    codons = separate_into_codons(dna_sequence)
    proteins = compute_sequence_proteins(codons)
    return(''.join(proteins))

def compute_dna_rates(dna_sequence):
    dna_rate = {"A":0,
                "T":0,
                "C":0,
                "G":0}
    for nuc in dna_sequence:
        if nuc!="N":
            dna_rate[nuc]+=1
    for key, value in dna_rate.items():
        if len(dna_sequence)!=0:
            dna_rate[key] = value/len(dna_sequence)

    return(dna_rate)

def compute_protein_rates(protein_sequence):
    prot_rates = {"A":0,
                  "R":0,
                  "D":0,
                  "N":0,
                  "C":0,
                  "E":0,
                  "Q":0,
                  "G":0,
                  "H":0,
                  "I":0,
                  "L":0,
                  "K":0,
                  "M":0,
                  "F":0,
                  "P":0,
                  "S":0,
                  "T":0,
                  "W":0,
                  "Y":0,
                  "V":0}
    
    for prot in protein_sequence:
        prot_rates[prot]+=1
    for key, value in prot_rates.items():
        if len(protein_sequence)!=0:
            prot_rates[key] = value/len(protein_sequence)
    return(prot_rates)

def compute_features(dna_sequence):
    # Compute the necessary features (this is a placeholder)
    protein_sequence = compute_protein(dna_sequence)
    features = {
        'len_DNA': len(dna_sequence),
        'DNA_sequence': dna_sequence,
        'DNA_rate_A': compute_dna_rates(dna_sequence)['A'],
        'DNA_rate_T': compute_dna_rates(dna_sequence)['T'],
        'DNA_rate_C': compute_dna_rates(dna_sequence)['C'],
        'DNA_rate_G': compute_dna_rates(dna_sequence)['G'],

        'len_proteins': len(protein_sequence),
        'Protein_sequence': protein_sequence,
        'prot_rates_A': compute_protein_rates(protein_sequence)['A'],
        'prot_rates_R': compute_protein_rates(protein_sequence)['R'],
        'prot_rates_D': compute_protein_rates(protein_sequence)['D'],
        'prot_rates_N': compute_protein_rates(protein_sequence)['N'],
        'prot_rates_C': compute_protein_rates(protein_sequence)['C'],
        'prot_rates_E': compute_protein_rates(protein_sequence)['E'],
        'prot_rates_Q': compute_protein_rates(protein_sequence)['Q'],
        'prot_rates_G': compute_protein_rates(protein_sequence)['G'],
        'prot_rates_H': compute_protein_rates(protein_sequence)['H'],
        'prot_rates_I': compute_protein_rates(protein_sequence)['I'],
        'prot_rates_L': compute_protein_rates(protein_sequence)['L'],
        'prot_rates_K': compute_protein_rates(protein_sequence)['K'],
        'prot_rates_M': compute_protein_rates(protein_sequence)['M'],
        'prot_rates_F': compute_protein_rates(protein_sequence)['F'],
        'prot_rates_P': compute_protein_rates(protein_sequence)['P'],
        'prot_rates_S': compute_protein_rates(protein_sequence)['S'],
        'prot_rates_T': compute_protein_rates(protein_sequence)['T'],
        'prot_rates_W': compute_protein_rates(protein_sequence)['W'],
        'prot_rates_Y': compute_protein_rates(protein_sequence)['Y'],
        'prot_rates_V': compute_protein_rates(protein_sequence)['V'],
    }
    return features

# Function to encode DNA sequences into indices
def encode_dna(sequence, max_length):
    chars = 'ACGT'
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    integer_encoded = [char_to_int[char] for char in sequence if char in char_to_int]
    while len(integer_encoded) < max_length:
        integer_encoded.append(0)
    return integer_encoded[:max_length]

# Function to encode protein sequences into indices
def encode_protein(sequence, max_length):
    chars = 'ACDEFGHIKLMNPQRSTVWY'  # 20 acides aminés standards
    char_to_int = dict((c, i) for i, c in enumerate(chars))
    integer_encoded = [char_to_int[char] for char in sequence if char in char_to_int]
    while len(integer_encoded) < max_length:
        integer_encoded.append(0)
    return integer_encoded[:max_length]

def preProcessing(DNA_seq):
    feature = compute_features(DNA_seq)
    df = pd.DataFrame([feature])
    
    sequence_columns = ['DNA_sequence', 'Protein_sequence']
    encoded_sequences = []
    for col in sequence_columns:
        if 'DNA' in col:
            encoded_col = df[col].apply(lambda x: encode_dna(x, max_seq_length))
        else:
            encoded_col = df[col].apply(lambda x: encode_protein(x, max_seq_length))
        encoded_sequences.append(np.array(encoded_col.tolist()))

    X_sequences = np.concatenate(encoded_sequences, axis=1)
    X = df.drop(columns=['DNA_sequence', 'Protein_sequence'])

    numeric_columns = X.select_dtypes(include=[np.number]).columns

    X[numeric_columns] = scaler.transform(X[numeric_columns])
    X_numeric = X.values
    X_combined = np.concatenate((X_numeric, X_sequences), axis=1)
    X_reshaped = np.reshape(X_combined, (X_combined.shape[0], 1, X_combined.shape[1]))
    return X_reshaped

def predict(dna_sequence):
    feature = compute_features(dna_sequence)
    df = pd.DataFrame([feature])
    x_pred_process = preProcessing(dna_sequence)
    prediction_go0 = model_lstm_go0.predict(x_pred_process)
    predicted_class_go0 = np.argmax(prediction_go0, axis=1)

    predicted_class_labels_go0 = le_lstm_go0.inverse_transform(predicted_class_go0)[0]

    predicted_class_go1 = model_knn_go1.predict(df)
    predicted_class_indices_go1 = np.argmax(predicted_class_go1, axis=1)
    predicted_class_labels_go1 = le_go1.inverse_transform(predicted_class_indices_go1)[0]
    namespace = namespaces[predicted_class_labels_go0]
    return(predicted_class_labels_go0, predicted_class_labels_go1, namespace, feature['Protein_sequence'])


# def predict(dna_sequence):
#     feature = compute_features(dna_sequence)
#     df = pd.DataFrame([feature])

#     predicted_class_go0 = model_knn_go0.predict(df)
#     predicted_class_indices_go0 = np.argmax(predicted_class_go0, axis=1)
#     predicted_class_labels_go0 = le_go0.inverse_transform(predicted_class_indices_go0)[0]

#     predicted_class_go1 = model_knn_go1.predict(df)
#     predicted_class_indices_go1 = np.argmax(predicted_class_go1, axis=1)
#     predicted_class_labels_go1 = le_go1.inverse_transform(predicted_class_indices_go1)[0]
#     namespace = namespaces[predicted_class_labels_go0]
#     return(predicted_class_labels_go0, predicted_class_labels_go1, namespace, feature['Protein_sequence'])