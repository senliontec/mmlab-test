import argparse

from mmengine.config import Config, DictAction


def parse_args():
    parser = argparse.ArgumentParser(description='Script Example')
    parser.add_argument('config',
                        help='train config file path')
    parser.add_argument('--cfg-options',
                        nargs='+',
                        action=DictAction,
                        help='')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    cfg = Config.fromfile(args.config)
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    print(cfg)


if __name__ == '__main__':
    main()
