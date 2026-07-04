/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:41 by Tsellak           #+#    #+#             */
/*   Updated: 2026/07/02 23:14:54 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long	ft_atol(char *str)
{
	long	num;
	int		i;

	num = 0;
	i = 0;
	if (str[0] == '+')
		i++;
	while (str[i])
	{
		num = num * 10 + (str[i] - '0');
		i++;
	}
	return (num);
}

static int	validate_args(char *argv[])
{
	int	i;
	int	j;

	i = 1;
	while (i <= 7)
	{
		j = 0;
		if (!argv[i] || argv[i][0] == '\0' || (argv[i][0] == '0' && i != 7))
			return (i);
		if (argv[i][0] == '-')
			return (i);
		if (argv[i][0] == '+')
			j = 1;
		if ((int)strlen(argv[i]) - (argv[i][0] == '+') > 18)
			return (i);
		while (argv[i][j])
		{
			if (argv[i][j] < '0' || argv[i][j] > '9')
				return (i);
			j++;
		}
		i++;
	}
	return (0);
}

static void	parse_args(const char *allow[], char *argv[], t_data *data)
{
	int	err;

	err = validate_args(argv);
	if (err)
		ft_exit("Not valid argumant %s = %s\n", allow[err - 1], argv[err]);
	if (ft_atol(argv[1]) > INT_MAX)
		ft_exit("Not valid argumant %s = %s\n", allow[0], argv[1]);
	if (ft_atol(argv[6]) > INT_MAX)
		ft_exit("Not valid argumant %s = %s\n", allow[5], argv[6]);
	data->num_coders = (int)ft_atol(argv[1]);
	data->time_to_burnout = ft_atol(argv[2]);
	data->time_to_compile = ft_atol(argv[3]);
	data->time_to_debug = ft_atol(argv[4]);
	data->time_to_refactor = ft_atol(argv[5]);
	data->num_compiles_required = (int)ft_atol(argv[6]);
	data->dongle_cooldown = ft_atol(argv[7]);
	if (strcmp(argv[8], "fifo") == 0)
		data->scheduler = 0;
	else if (strcmp(argv[8], "edf") == 0)
		data->scheduler = 1;
	else
		ft_exit("Error: scheduler must be 'fifo' or 'edf'\n", NULL, NULL);
}

static void	check_arguments(int argc, char *argv[], const char *allow[])
{
	int	i;
	int	missing;

	i = 0;
	missing = argc - 1;
	if (argc > 9)
	{
		printf("Usage: %s", argv[0]);
		while (i < 8)
			printf(" %s", allow[i++]);
	}
	else
	{
		printf("Missing:");
		while (i <= missing)
			printf(" %s", argv[i++]);
		while (missing < 8)
			printf(" %s", allow[missing++]);
	}
	printf("\n");
	exit(1);
}

int	main(int argc, char *argv[])
{
	t_data		data;
	const char	*allow[] = {"number_of_coders", "time_to_burnout",
		"time_to_compile", "time_to_debug", "time_to_refactor",
		"number_of_compiles_required", "dongle_cooldown", "scheduler"};

	if (argc != 9)
		check_arguments(argc, argv, allow);
	parse_args(allow, argv, &data);
	if (start_threads(&data))
		ft_exit("Error: memory allocation failed\n", NULL, NULL);
	cleanup_all(&data);
	return (0);
}
