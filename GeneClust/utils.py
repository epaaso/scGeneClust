# -*- coding: utf-8 -*-
# @Time : 2022/4/11 17:33
# @Author : Tory Deng
# @File : utils.py
# @Software: PyCharm

import anndata as ad
from typing import Union
import numpy as np
import pandas as pd


def subset_adata(adata: ad.AnnData, selected_genes: Union[np.ndarray, pd.Index], inplace=False):
    if isinstance(selected_genes, pd.Index):
        selected_genes = selected_genes.to_numpy()
    gene_mask = adata.var_names.isin(selected_genes)
    if inplace:
        if adata.raw is not None:
            adata.raw = adata.raw[:, gene_mask].to_adata()
            if adata.raw.shape[1] != selected_genes.shape[0]:
                raise RuntimeError(f"{adata.raw.shape[1]} genes in raw data were selected, "
                                   f"not {selected_genes.shape[0]} genes. Please check the gene names.")
        adata._inplace_subset_var(selected_genes)
        if adata.shape[1] != selected_genes.shape[0]:
            raise RuntimeError(
                f"{adata.shape[1]} in norm data were selected, "
                f"not {selected_genes.shape[0]} genes. Please check the gene names."
            )
    else:
        copied_adata = adata.copy()
        subset_adata(copied_adata, selected_genes, inplace=True)
        return copied_adata
