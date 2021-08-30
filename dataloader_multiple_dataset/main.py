import argparse
import torch
import os
from torchvision import datasets, transforms
from torchvision.datasets.folder import ImageFolder, default_loader
import time

def get_args_parser():
    parser = argparse.ArgumentParser('Dataloader for multiple datasets', add_help=False)
    parser.add_argument('--distributed', default=False, type=bool, help='use distributed processing or not')
    parser.add_argument('--batch_size', default=128, type=int)
    parser.add_argument('--epochs', default=10, type=int)
    parser.add_argument('--num_workers', default=10, type=int)
    parser.add_argument('--pin-mem', action='store_true',
                        help='Pin CPU memory in DataLoader for more efficient (sometimes) transfer to GPU.')
    parser.add_argument('--no-pin-mem', action='store_false', dest='pin_mem', help='')
    parser.set_defaults(pin_mem=True)

    parser.add_argument('--data-path', default='/path/to/data/', type=str, help='dataset path')
    parser.add_argument('--data-set', default='BU4DFE', choices=['BU4DFE', 'BU3DFE', 'Bosphorous', 'BP4D'],
                        type=str, help='Corresponding dataset path')
    opt = parser.parse_args()
    opt.data_path_base = ''  # path to base dataset 

    return opt

def build_dataset(is_train, args, transform=None):
    if args.data_set == 'BU4DFE':
        root = os.path.join(args.data_path, 'train' if is_train else 'val')
        dataset = datasets.ImageFolder(root, transform=transform)
        nb_classes = 6
    elif args.data_set == 'BU3DFE':
        root = os.path.join(args.data_path, 'train' if is_train else 'val')
        dataset = datasets.ImageFolder(root, transform=transform)
        nb_classes = 6
    elif args.data_set == 'Bosphorous':
        root = os.path.join(args.data_path, 'train' if is_train else 'val')
        dataset = datasets.ImageFolder(root, transform=transform)
        nb_classes = 6
    elif args.data_set == 'BP4D':
        root = os.path.join(args.data_path, 'train' if is_train else 'val')
        dataset = datasets.ImageFolder(root, transform=transform)
        nb_classes = 8
    else:
        NotImplemented("Implementation not yet supported.")

    return dataset, nb_classes

class ConcatDataset(torch.utils.data.Dataset):
    def __init__(self, *datasets):
        self.datasets = datasets

    def __getitem__(self, i):
        return tuple(d[i] for d in self.datasets)

    def __len__(self):
        return min(len(d) for d in self.datasets)


def main():
    args = get_args_parser()
    RA_views = ['Front', 'Left', 'Right']

    args.data_path = os.path.join(args.data_path_base, RA_views[0])
    dataset_trainRA0, args.nb_classesRA0 = build_dataset(is_train=True, args=args, transform=None)
    dataset_valRA0, _ = build_dataset(is_train=False, args=args)

    args.data_path = os.path.join(args.data_path_base, RA_views[1])
    dataset_trainRA20, args.nb_classesRA20 = build_dataset(is_train=True, args=args, transform=None)
    dataset_valRA20, _ = build_dataset(is_train=False, args=args)

    args.data_path = os.path.join(args.data_path_base, RA_views[2])
    dataset_trainRA_20, args.nb_classesRA_20 = build_dataset(is_train=True, args=args, transform=None)
    dataset_valRA_20, _ = build_dataset(is_train=False, args=args)

    assert args.nb_classesRA0 == args.nb_classesRA20 and args.nb_classesRA0 == args.nb_classesRA_20
    args.nb_classes = args.nb_classesRA_20
    del args.nb_classesRA0, args.nb_classesRA20, args.nb_classesRA_20, args.data_path


    for RA_iter in range(len(RA_views)):
        if RA_iter == 0:
            dataset_train = dataset_trainRA0
            dataset_val = dataset_valRA0
        elif RA_iter == 1:
            dataset_train = dataset_trainRA20
            dataset_val = dataset_valRA20
        elif RA_iter == 2:
            dataset_train = dataset_trainRA_20
            dataset_val = dataset_valRA_20
        else:
            ValueError('Invalid indexing')


        if args.distributed:
            num_tasks = world_size # need to define
            global_rank = rank_num # need to define

            sampler_train = torch.utils.data.DistributedSampler(
                        dataset_train, num_replicas=num_tasks, rank=global_rank, shuffle=True)
        else:
            sampler_train = torch.utils.data.RandomSampler(dataset_train)
        
        sampler_val = torch.utils.data.SequentialSampler(dataset_val)

        data_loader_train = torch.utils.data.DataLoader(
            dataset_train, sampler=sampler_train,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            pin_memory=args.pin_mem,
            drop_last=True,
        )

        data_loader_val = torch.utils.data.DataLoader(
            dataset_val, sampler=sampler_val,
            batch_size=int(1.5 * args.batch_size),
            num_workers=args.num_workers,
            pin_memory=args.pin_mem,
            drop_last=False
        )

        if RA_iter == 0:
            data_loader_trainRA0 = data_loader_train
            data_loader_valRA0 = data_loader_val
        elif RA_iter == 1:
            data_loader_trainRA20 = data_loader_train
            data_loader_valRA20 = data_loader_val
        elif RA_iter == 2:
            data_loader_trainRA_20 = data_loader_train
            data_loader_valRA_20 = data_loader_val
        else:
            ValueError('Invalid indexing')

        del data_loader_train, data_loader_val, dataset_train, dataset_val
    del dataset_trainRA0, dataset_valRA0, dataset_trainRA20, dataset_valRA20, dataset_trainRA_20, dataset_valRA_20

    transform = transforms.Compose([transforms.ToTensor()])

    traindirRA0 = os.path.join(args.data_path_base, RA_views[0], 'train')
    traindirRA20 = os.path.join(args.data_path_base, RA_views[1], 'train')    
    traindirRA_20 = os.path.join(args.data_path_base, RA_views[2], 'train')
    train_loader = torch.utils.data.DataLoader(
             ConcatDataset(
                 datasets.ImageFolder(traindirRA0, transform=transform),
                 datasets.ImageFolder(traindirRA20, transform=transform),
                 datasets.ImageFolder(traindirRA_20, transform=transform)
                 ),
             batch_size=args.batch_size, shuffle=True,
             num_workers=args.num_workers, pin_memory=True)
    
    
    valdirRA0 = os.path.join(args.data_path_base, RA_views[0], 'val')
    valdirRA20 = os.path.join(args.data_path_base, RA_views[1], 'val')    
    valdirRA_20 = os.path.join(args.data_path_base, RA_views[2], 'val')
    val_loader = torch.utils.data.DataLoader(
             ConcatDataset(
                 datasets.ImageFolder(valdirRA0, transform=transform),
                 datasets.ImageFolder(valdirRA20, transform=transform),
                 datasets.ImageFolder(valdirRA_20, transform=transform)
                 ),
             batch_size=int(1.5*args.batch_size), shuffle=False,
             num_workers=args.num_workers, pin_memory=True)

    for epoch in range(args.epochs):
        print()
        for i, ((input1, target1), (input2, target2), (input3, target3))  in enumerate(train_loader):
            assert torch.equal(target1, target2) and torch.equal(target1, target3)
            print("Training [epoch={}]: [{}]/[{}]".format(epoch,
                (i+1)*len(target1) if len(target1)==args.batch_size else i*args.batch_size + len(target1), 
                len(train_loader.dataset)))
            time.sleep(1)

            # code to train data

        print()
        for i, ((input1, target1), (input2, target2), (input3, target3))  in enumerate(val_loader):
            assert torch.equal(target1, target2) and torch.equal(target1, target3)
            print("Testing: [{}]/[{}]".format(
                (i+1)*len(target1) if len(target1)==int(1.5*args.batch_size) else i*int(1.5*args.batch_size) + len(target1),
                len(val_loader.dataset)))
            time.sleep(1)

            # code to validate data

    return


if __name__ == '__main__':
    main()
