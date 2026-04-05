/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 23:17:25 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/01 21:44:03 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	long	nmbr;
	char	ch;

	nmbr = n;
	if (nmbr < 0)
	{
		ft_putchar_fd('-', fd);
		nmbr = -nmbr;
	}
	if (nmbr > 9)
		ft_putnbr_fd(nmbr / 10, fd);
	ch = (nmbr % 10) + '0';
	ft_putchar_fd(ch, fd);
}
