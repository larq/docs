from keras_autodoc import DocumentationGenerator, get_classes, get_functions

repo_apis = {
    "larq": {
        "layers.md": [
            "larq.layers.QuantDense",
            "larq.layers.QuantConv1D",
            "larq.layers.QuantConv2D",
            "larq.layers.QuantConv3D",
            "larq.layers.QuantDepthwiseConv2D",
            "larq.layers.QuantSeparableConv1D",
            "larq.layers.QuantSeparableConv2D",
            "larq.layers.QuantConv2DTranspose",
            "larq.layers.QuantConv3DTranspose",
            "larq.layers.QuantLocallyConnected1D",
            "larq.layers.QuantLocallyConnected2D",
        ],
        "activations.md": get_functions("larq.activations"),
        "callbacks.md": get_classes("larq.callbacks"),
        "constraints.md": get_classes("larq.constraints"),
        "context.md": get_functions("larq.context"),
        "optimizers.md": ["larq.optimizers.CaseOptimizer", "larq.optimizers.Bop"],
        "math.md": get_functions("larq.math"),
        "models.md": ["larq.models.summary"],  #  parse error, suspecting `print`
        "metrics.md": get_classes("larq.metrics"),
        "quantizers.md": [
            "larq.quantizers.NoOpQuantizer",
            "larq.quantizers.SteSign",
            "larq.quantizers.ApproxSign",
            "larq.quantizers.SteHeaviside",
            "larq.quantizers.SwishSign",
            "larq.quantizers.MagnitudeAwareSign",
            "larq.quantizers.SteTern",
            "larq.quantizers.DoReFaQuantizer",
        ],
    },
    "zoo": {
        "index.md": ["larq_zoo.decode_predictions", "larq_zoo.preprocess_input"],
        "literature.md": [
            "larq_zoo.literature.BinaryAlexNet",
            "larq_zoo.literature.BiRealNet",
            "larq_zoo.literature.BinaryResNetE18",
            "larq_zoo.literature.BinaryDenseNet28",
            "larq_zoo.literature.BinaryDenseNet37",
            "larq_zoo.literature.BinaryDenseNet37Dilated",
            "larq_zoo.literature.BinaryDenseNet45",
            "larq_zoo.literature.DoReFaNet",
            "larq_zoo.literature.XNORNet",
        ],
        "sota.md": [
            "larq_zoo.sota.QuickNet",
            "larq_zoo.sota.QuickNetLarge",
            "larq_zoo.sota.QuickNetXL",
        ],
    },
    "compute-engine": {"index.md": ["larq_compute_engine.convert_keras_model"]},
}

for repo, api_pages in repo_apis.items():
    doc_generator = DocumentationGenerator(
        api_pages,
        project_url=f"https://github.com/larq/{repo}/blob/master/",
        template_dir=f"./docs/{repo}/api_page_templates" if repo == "larq" else None,
        extra_aliases={
            "tensorflow.python.ops.variables.Variable": "tf.Variable",
            "tensorflow.python.keras.optimizer_v2.optimizer_v2.OptimizerV2": "tf.keras.optimizers.Optimizer",
        },
        max_signature_line_length=88,
    )
    doc_generator.generate(f"./docs/{repo}/api")
